from flask import Flask, render_template, redirect, request, url_for
from flask import g, session, flash, jsonify, make_response, abort
from pymongo import MongoClient, ASCENDING, DESCENDING

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
    items = list(g.db.todo.items.find().sort('order', ASCENDING))
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add_item():
    if not session.get('logged_in'):
        abort(401)

    try:
        progress = float(request.form['progress'])
    except ValueError:
        flash("Invalid value for progress")
        return redirect(url_for('root'))

    last_item = next(g.db.todo.items.find().sort('order', DESCENDING))
    order = last_item['order'] + 1
    g.db.todo.items.insert({'_id': request.form['name'],
                            'progress': progress,
                            'description': request.form['description'],
                            'order': order})
    return redirect(url_for('root'))

@app.route('/move_down', methods=['POST'])
def move_down():
    db_item = g.db.todo.items.find_one({'_id': request.form['item']})
    order = db_item['order']
    next_item = g.db.todo.items.find_one({'order': order + 1})

    if next_item is None:
        return make_response(jsonify({'error': 'last item'}), 400)

    g.db.todo.items.update({'_id': db_item['_id']}, {'$inc': {'order': 1}})
    g.db.todo.items.update({'_id': next_item['_id']}, {'$inc': {'order': -1}})
    # Just assuming it works...
    return jsonify({'result': True})

@app.route('/move_up', methods=['POST'])
def move_up():
    db_item = g.db.todo.items.find_one({'_id': request.form['item']})
    order = db_item['order']
    prev_item = g.db.todo.items.find_one({'order': order - 1})

    if prev_item is None:
        return make_response(jsonify({'error': 'last item'}), 400)

    g.db.todo.items.update({'_id': db_item['_id']}, {'$inc': {'order': -1}})
    g.db.todo.items.update({'_id': prev_item['_id']}, {'$inc': {'order': 1}})
    # Just assuming it works...
    return jsonify({'result': True})

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
