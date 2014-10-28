from flask import Flask, render_template, g
from pymongo import MongoClient

DATABASE = 'mongodb://localhost:27017/'

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

if __name__ == '__main__':
    app.run(debug=True)
