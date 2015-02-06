# -*- coding: utf-8 -*-
# encoding: utf-8

from flask import Flask, session, request, render_template
from urllib2 import Request, urlopen
import os
import json
from json import dumps

app = Flask(__name__)
app.secret_key = os.urandom(24)
prefix = "/~jereczem/apps/CW5"
app.debug = True

@app.route(prefix + '/')
def index():
    return render_template('menu.html')

@app.route(prefix + '/cat/<category>')
def indcat(category):
    return render_template('category.html', category=category)

@app.route(prefix + '/lab/<label>')
def indlab(label):
    return render_template('label.html', label=label)

@app.route(prefix + '/refresh/', methods=['GET'])
def refresh():
    request = Request("http://len.iem.pw.edu.pl/~jereczem/apps/noteapp/note/")
    response_body = urlopen(request).read()
    notes = json.loads(response_body)
    result = ""
    for note in notes:
        result += "<div class=note>"
        result += "<div class=category>"
        result += "<p>Kategoria: " + str(note['category']) + "</p>"
        result += "</div>"
        result += "<div class=labels>"
        result += "<p>Etykiety: " + str(note['labels']) + "</p>"
        result += "</div>"
        result += "<div class=note_text>"
        result += "<p> Tresc: " + str(note['note_text']) + "</p>"
        result += "</div>"
        result += "<div class=delete>"

        result += "<a href=\"javascript:window.open('http://len.iem.pw.edu.pl/~jereczem/apps/CW5/delete_note/"
        result += "?note_id=" + str(note["note_id"])
        result += "','Usunięcie notatki','width=500,height=300')\">Usuń</a>"

        result += "<a href=\"javascript:window.open('http://len.iem.pw.edu.pl/~jereczem/apps/CW5/edit_note/"
        result += "?note_id=" + str(note["note_id"])
        result += "&category=" + str(note["category"])
        result += "&labels=" + str(note["labels"])
        result += "&note_text=" + str(note["note_text"])
        result += "','Usunięcie notatki','width=500,height=300')\">Edytuj</a>"

        result += "</div>"
        result += "</div>"
    return result

@app.route(prefix + '/category/<category>', methods=['GET'])
def category(category):
    request = Request("http://len.iem.pw.edu.pl/~jereczem/apps/noteapp/note/category/" + str(category))
    response_body = urlopen(request).read()
    notes = json.loads(response_body)
    result = ""
    for note in notes:
        result += "<div class=note>"
        result += "<div class=category>"
        result += "<p>Kategoria: " + str(note['category']) + "</p>"
        result += "</div>"
        result += "<div class=labels>"
        result += "<p>Etykiety: " + str(note['labels']) + "</p>"
        result += "</div>"
        result += "<div class=note_text>"
        result += "<p> Tresc: " + str(note['note_text']) + "</p>"
        result += "</div>"
        result += "<div class=delete>"

        result += "<a href=\"javascript:window.open('http://len.iem.pw.edu.pl/~jereczem/apps/CW5/delete_note/"
        result += "?note_id=" + str(note["note_id"])
        result += "','Usunięcie notatki','width=500,height=300')\">Usuń</a>"

        result += "<a href=\"javascript:window.open('http://len.iem.pw.edu.pl/~jereczem/apps/CW5/edit_note/"
        result += "?note_id=" + str(note["note_id"])
        result += "&category=" + str(note["category"])
        result += "&labels=" + str(note["labels"])
        result += "&note_text=" + str(note["note_text"])
        result += "','Usunięcie notatki','width=500,height=300')\">Edytuj</a>"

        result += "</div>"
        result += "</div>"
    return result

@app.route(prefix + '/label/<label>', methods=['GET'])
def label(label):
    request = Request("http://len.iem.pw.edu.pl/~jereczem/apps/noteapp/note/label/" + str(label))
    response_body = urlopen(request).read()
    notes = json.loads(response_body)
    result = ""
    for note in notes:
        result += "<div class=note>"
        result += "<div class=category>"
        result += "<p>Kategoria: " + str(note['category']) + "</p>"
        result += "</div>"
        result += "<div class=labels>"
        result += "<p>Etykiety: " + str(note['labels']) + "</p>"
        result += "</div>"
        result += "<div class=note_text>"
        result += "<p> Tresc: " + str(note['note_text']) + "</p>"
        result += "</div>"
        result += "<div class=delete>"

        result += "<a href=\"javascript:window.open('http://len.iem.pw.edu.pl/~jereczem/apps/CW5/delete_note/"
        result += "?note_id=" + str(note["note_id"])
        result += "','Usunięcie notatki','width=500,height=300')\">Usuń</a>"

        result += "<a href=\"javascript:window.open('http://len.iem.pw.edu.pl/~jereczem/apps/CW5/edit_note/"
        result += "?note_id=" + str(note["note_id"])
        result += "&category=" + str(note["category"])
        result += "&labels=" + str(note["labels"])
        result += "&note_text=" + str(note["note_text"])
        result += "','Usunięcie notatki','width=500,height=300')\">Edytuj</a>"

        result += "</div>"
        result += "</div>"
    return result

@app.route(prefix + '/refresh_cat/', methods=['GET'])
def refresh_cat():
    request = Request("http://len.iem.pw.edu.pl/~jereczem/apps/noteapp/category/")
    response_body = urlopen(request).read()
    categories = json.loads(response_body)
    result = ""
    for category in categories:
        result += '<a href="http://len.iem.pw.edu.pl/~jereczem/apps/CW5/cat/' + str(category) + '">'
        result += str(category) + "</a> "
    return result

@app.route(prefix + '/refresh_lab/', methods=['GET'])
def refresh_lab():
    request = Request("http://len.iem.pw.edu.pl/~jereczem/apps/noteapp/label/")
    response_body = urlopen(request).read()
    labels = json.loads(response_body)
    result = ""
    for label in labels:
        result += '<a href="http://len.iem.pw.edu.pl/~jereczem/apps/CW5/lab/' + str(label) + '">'
        result += str(label) + "</a> "
    return result

@app.route(prefix + '/delete_note/', methods=['GET'])
def delete_note():
        note_id = request.args.get('note_id')
        rq = Request("http://len.iem.pw.edu.pl/~jereczem/apps/noteapp/note/" + str(note_id))
        rq.get_method = lambda: 'DELETE'
        response_body = urlopen(rq).read()
        if str(response_body) == "404":
            return "nie można usunąć tej wiadomości.."
        return "usunięto wiadomość"

@app.route(prefix + '/edit_note/', methods=['GET'])
def edit_note():
        note_id = request.args.get('note_id')
        category = request.args.get('category')
        labels = request.args.get('labels')
        note_text = request.args.get('note_text')
        return render_template('editnote.html', note_id=note_id, category=category, labels=labels, note_text=note_text)

@app.route(prefix + '/newnote/', methods=['GET'])
def newnote():
        return render_template('newnote.html')


if __name__ == '__main__':
    app.run()

