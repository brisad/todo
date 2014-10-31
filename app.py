from flask import Flask, render_template, redirect, request, url_for
from flask import g, session, flash
from pymongo import MongoClient

DATABASE = 'mongodb://localhost:27017/'
SECRET_KEY = 'temporary_secret'
DEBUG = True
USERNAME = 'michael'
PASSWORD = 'secret'

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    return MongoClient(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def root():
    items = list(g.db.todo.items.find())
    return render_template('index.html', items=items)

@app.route('/login', methods=['POST'])
def login():
    if (request.form['username'] != app.config['USERNAME'] or
        request.form['password'] != app.config['PASSWORD']):
        flash('Invalid username or password')
    else:
        session['logged_in'] = True
    return redirect(url_for('root'))

@app.route('/logout')
def logout():
    del session['logged_in']
    return redirect(url_for('root'))

if __name__ == '__main__':
    app.run()
