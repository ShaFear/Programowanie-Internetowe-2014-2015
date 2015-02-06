# -*- coding: utf-8 -*-

from flask import Flask, session, url_for, request, render_template
import json
import os

notes = []

app = Flask(__name__)
app.secret_key = os.urandom(24)
prefix = "/~jereczem/apps/noteapp"
app.debug = True

# wyświetla wszystkie notatki
@app.route(prefix + '/note/', methods=['GET'])
def get_notes():
    return str(json.dumps(notes))

# tworzy nową notatkę
@app.route(prefix + '/note/', methods=['POST'])
def post_note():
    category = request.form['category']
    labels = request.form['labels']
    note_text = request.form['note_text']
    note_id = len(notes) + 1
    notes.insert(0, {"note_id": note_id, "category": category, "labels": labels, "note_text": note_text})
    return "Pomyślnie dodano wiadomość"

# wyświetla wszystkie kategorie
@app.route(prefix + '/category/', methods=['GET'])
def get_categories():
    categories = []
    for note in notes:
        if not note['category'] in categories:
            categories.insert(0, note['category'])
    return str(json.dumps(categories))

# wyświetla wszystkie etykiety
@app.route(prefix + '/label/', methods=['GET'])
def get_labels():
    labels = []
    for note in notes:
        note_labels = note['labels'].split(';')
        for note_label in note_labels:
            if not note_label in labels:
                labels.insert(0, note_label)
    return str(json.dumps(labels))

# wyświetla konkretną notatkę
@app.route(prefix + '/note/<note_id>', methods=['GET'])
def get_note(note_id):
    for note in notes:
        if str(note['note_id']) == str(note_id):
            return str(json.dumps(note))
    return "404"

# edytuje konkretną notatkę
@app.route(prefix + '/edit_note/<note_id>', methods=['POST'])
def edit_note(note_id):
    for note in notes:
        if str(note['note_id']) == str(note_id):
            category = request.form['category']
            labels = request.form['labels']
            note_text = request.form['note_text']
            note['category'] = category
            note['labels'] = labels
            note['note_text'] = note_text
            return "Pomyślnie edytowano notatkę"
    return "Nie można edytować notatki - nie znaleziono"

# usuwa konkretną notatkę
@app.route(prefix + '/note/<note_id>', methods=['DELETE'])
def delete_note(note_id):
    for note in notes:
        if str(note['note_id']) == str(note_id):
            notes.remove(note)
            return "200"
    return "404"

# wyświetla wszystkie wiadomosci z dana etykieta
@app.route(prefix + '/note/label/<label_name>', methods=['GET'])
def get_label(label_name):
    label_notes = []
    for note in notes:
        note_labels = note['labels'].split(';')
        for note_label in note_labels:
            if str(note_label) == str(label_name):
                label_notes.insert(0, note)
                break
    return json.dumps(label_notes)

# wyświetla wszystkie wiadomosci z dana kategoria
@app.route(prefix + '/note/category/<category_name>', methods=['GET'])
def get_category(category_name):
    category_notes = []
    for note in notes:
        if str(note['category']) == str(category_name):
            category_notes.insert(0, note)
    return json.dumps(category_notes)


if __name__ == '__main__':
    app.run()

