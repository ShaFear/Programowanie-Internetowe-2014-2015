# -*- coding: utf-8 -*-
# encoding: utf-8

from flask import Flask, session, request, render_template
from urllib2 import Request, urlopen
import os
import json
from json import dumps

app = Flask(__name__)
app.secret_key = os.urandom(24)
prefix = "/~jereczem/apps/CW4"
app.debug = True

#sprawdza czy uzytkownik jest w bazie
def check_username(username):
    try:
        #logowanie
        values = username
        headers = {"Content-Type": "text/plain"}
        rq = Request("http://len.iem.pw.edu.pl/staff/~chaberb/apps/mail/login/" + values, data=values, headers=headers)
        response_body = urlopen(rq).read()
        jsondata = json.loads(response_body);
        msg = jsondata.get('msg')
        if msg != "credentials correct":
            return '0'
        session['id'] = jsondata.get('user_id')
        return '1'
    except:
        return '0'

#zwraca informacje o uzytkowniku w jsonie
def get_user_information_from_id(id):
    request = Request("http://len.iem.pw.edu.pl/staff/~chaberb/apps/mail/user")
    response_body = urlopen(request).read()
    jsondata = json.loads(response_body)
    for user in jsondata:
        if user["user_id"] == id:
            return user["username"]
    return "problem"


#zwraca dane o mailach od/do zalogowanego uzytkownika (od razu zmienia ID na imiona)
def get_email_list(id):
    request = Request("http://len.iem.pw.edu.pl/staff/~chaberb/apps/mail/user/" + str(session['id']) + "/messages")
    response_body = urlopen(request).read()
    jsondata = json.loads(response_body)
    for email in jsondata:
        try:
            email['to_user_id'] = str(get_user_information_from_id(email['to_user_id']))
            email['from_user_id'] = str(get_user_information_from_id(email['from_user_id']))
        except:
            return jsondata
    return jsondata

#zwraca dane o mailach od/do zalogowanego uzytkownika (od razu zmienia ID na imiona) bez JSONA (string)
def get_email_list_string(id):
    request = Request("http://len.iem.pw.edu.pl/staff/~chaberb/apps/mail/user/" + str(id) + "/messages")
    response_body = urlopen(request).read()
    jsondata = json.loads(response_body)
    result = ""
    for email in jsondata:
        try:
            result += "<div class=message>"
            email['to_user_id'] = str(get_user_information_from_id(email['to_user_id']))
            email['from_user_id'] = str(get_user_information_from_id(email['from_user_id']))
            result += "<div class=\"sender\"><p> Od: " + str(email['from_user_id']) + "</p></div>"
            result += "<div class=\"receiver\"><p> Do: " + str(email['to_user_id']) + "</p></div>"
            result += "<div class=\"emailtitle\">"
            if email["unread"] == 1:
                result += "<b>"
            result += "<div class=\"title\">"
            result += "<a href=\"javascript:window.open('http://len.iem.pw.edu.pl/~jereczem/apps/CW4/readmail/"
            result += "?message_id=" + str(email["message_id"])
            result += "','Usunięcie wiadomości','width=500,height=300')\">" + str(email["title"]) + "</a></div>"
            if email["unread"] == 1:
                result += "</b>"
            result += "</div>"

            result += "<div class=\"delete\">"
            result += "<a href=\"javascript:window.open('http://len.iem.pw.edu.pl/~jereczem/apps/CW4/deletemail/"
            result += "?message_id=" + str(email["message_id"])
            result += "','Usunięcie wiadomości','width=500,height=300')\">Usuń</a></div></div>"
        except:
            return result + "</div>"
    return result + "</div>"

#zwaca informacje o mailu od razu podstawiajac nazwy pod id adresata/odbiorcy
#jezeli zalogowany uzytkownik jest adresatem to oznacza jako przeczytane
def get_email_from_id(message_id):
    request = Request("http://len.iem.pw.edu.pl/staff/~chaberb/apps/mail/msg/" + str(message_id))
    response_body = urlopen(request).read()
    jsondata = json.loads(response_body)
    jsondata['to_user_id'] = get_user_information_from_id(jsondata.get('to_user_id'))
    jsondata['from_user_id'] = get_user_information_from_id(jsondata.get('from_user_id'))
    try:
        if jsondata.get("to_user_id") == session['username']:
            request = Request("http://len.iem.pw.edu.pl/staff/~chaberb/apps/mail/msg/" + message_id + "/read")
            response_body = urlopen(request).read()
        return jsondata
    except:
        return jsondata

#wysyla wiadomosc (uwaga, nalezy wczesniej sprawdzic zy userzy o danym id istnieja!
def send_mail(content, to_user_id, title):
    values = dumps({"content": str(content), "to_user_id": to_user_id, "title": str(title),
                    "from_user_id": session['id']})
    headers = {"Content-Type": "application/json"}
    request = Request("http://len.iem.pw.edu.pl/staff/~chaberb/apps/mail/msg", data=values, headers=headers)
    response_body = urlopen(request).read()
    return response_body

#zmienia nazwe uzytkownika na id
def change_name_to_id(name):
    request = Request("http://len.iem.pw.edu.pl/staff/~chaberb/apps/mail/user")
    response_body = urlopen(request).read()
    jsondata = json.loads(response_body)
    for user in jsondata:
        if user["username"] == name:
            return user["user_id"]
    return 0

#sprawdzenie czy jest sie juz zalogowanym
@app.route(prefix + '/')
def start():
    try:
        if check_username(session['username']) == '1':
            return render_template('menu.html')
        return render_template('login.html')
    except:
        return render_template('login.html')

#logowanie sie
@app.route(prefix + '/login/', methods=['POST'])
def login():
    session['username'] = request.form['username']
    if check_username(session['username']) == '1':
        return render_template('menu.html', maillist=get_email_list(session['id']))
    return render_template('login.html')

#wylogowanie sie
@app.route(prefix + '/logout/', methods=['POST'])
def logout():
    session.pop('username', None)
    session.pop('id', None)
    return render_template('login.html')

#nowy email
@app.route(prefix + '/newmail/', methods=['GET'])
def newmail():
    try:
        if check_username(session['username']) == '1':
            return render_template('newmail.html')
        return render_template('login.html')
    except:
        return render_template('login.html')

#przeczytaj istniejacy email
@app.route(prefix + '/readmail/', methods=['GET'])
def readmail():
    message_id = request.args.get('message_id')
    emaildata = get_email_from_id(message_id)
    try:
        if check_username(session['username']) == '1':
            return render_template('readmail.html', emaildata=emaildata)
        return render_template('login.html')
    except:
        return render_template('login.html')

@app.route(prefix + '/deletemail/', methods=['GET'])
def deletemail():
    try:
        message_id = request.args.get('message_id')
        rq = Request("http://len.iem.pw.edu.pl/staff/~chaberb/apps/mail/msg/" + message_id)
        rq.get_method = lambda: 'DELETE'
        response_body = urlopen(rq).read()
        return "usunięto wiadomość"
    except :
        return "nie można usunąć tej wiadomości.."

@app.route(prefix + '/sendmail/', methods=['POST'])
def sendmail():
    try:
        receiver = change_name_to_id(request.form['receiver'])
        if receiver == 0:
            return "nie można wysłać maila, błędny adresat.."
        send_mail(request.form['content'], receiver, request.form['title'])
        return "wysłano maila"
    except:
        return "nie można wysłać maila.."

@app.route(prefix + '/refresh/', methods=['GET'])
def refresh():
    return get_email_list_string(session['id'])

if __name__ == '__main__':
    app.run()

