# -*- coding: utf-8 -*-

from flask import Flask, session, url_for, request, render_template
import os, time
from datetime import timedelta

app = Flask(__name__)
app.secret_key = os.urandom(24)
prefix = "/~jereczem/apps/CW3"
app.debug = True
db = {'admin': 'admin', 'chaberb': 'piesel'}
app.permanent_session_lifetime = timedelta(minutes=120)

def check_in_db(login, password, database):
    if login in database:
        if password == database[login]:
            return True
    return False

@app.route(prefix + '/')
def form():
    try:
        if check_in_db(session['login'], session['password'], db):
            f = open(session['login'])
            data = f.read()
            f.close()
            return render_template('form_action.html', login=session['login'], lastdate=data)
    except:
        return render_template('form_submit.html')

@app.route(prefix + '/logged/', methods=['POST'])
def logged():
    session['login'] = request.form['login']
    login = session['login']
    session['password'] = request.form['password']
    if check_in_db(session['login'], session['password'], db):
        try:
            f = open(session['login'])
            data = f.read()
            f.close()
        except:
            data = "brak"
        f = open(session['login'], "w")
        f.write(time.strftime('%c'))
        f.close()
        return render_template('form_action.html', login=session['login'], lastdate=data)
    return render_template('form_submit.html')

@app.route(prefix + '/', methods=['POST'])
def logout():
    session.pop('login', None)
    session.pop('password', None)
    return render_template('form_submit.html')

if __name__ == '__main__':
    app.run()

