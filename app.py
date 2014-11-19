from flask import Flask, render_template, redirect, request, url_for
from flask import g, session, flash, jsonify, make_response, abort
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import PyMongoError

DATABASE = 'mongodb://localhost:27017/'
SECRET_KEY = 'temporary_secret'
DEBUG = True
USERNAME = 'michael'
PASSWORD = 'secret'

app = Flask(__name__)
app.config.from_object(__name__)


class DataError(Exception):
    pass


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
        if progress < 0:
            progress = 0
        if progress > 1:
            progress = 1
    except ValueError:
        flash("Invalid value for progress")
        return redirect(url_for('root'))

    one_sorted_item = list(g.db.todo.items.find().sort('order', DESCENDING).limit(1))
    if one_sorted_item:
        order = one_sorted_item[0]['order'] + 1
    else:
        order = 0

    try:
        g.db.todo.items.insert({'_id': request.form['name'],
                                'progress': progress,
                                'description': request.form['description'],
                                'order': order})
    except PyMongoError:
        flash("Failed to add item")
        return redirect(url_for('root'))

    return redirect(url_for('root'))

@app.route('/remove', methods=['POST'])
def remove_item():
    if not session.get('logged_in'):
        abort(401)

    db_item = g.db.todo.items.find_one({'_id': request.form['item']})
    if db_item is None:
        return make_response(jsonify({'error': 'invalid item'}), 400)

    order = db_item['order']
    g.db.todo.items.remove({'_id': request.form['item']})

    g.db.todo.items.update({'order': {'$gt': order}}, {'$inc': {'order': -1}})
    return jsonify({'result': True})

def reorder(direction, name):
    db_item = g.db.todo.items.find_one({'_id': name})
    if db_item is None:
        raise DataError('invalid item')

    if direction == 'up':
        offset = -1
    else:
        offset = 1

    order = db_item['order']
    other_item = g.db.todo.items.find_one({'order': order + offset})

    if other_item is None:
        if direction == 'up':
            raise DataError('first item')
        else:
            raise DataError('last item')

    g.db.todo.items.update(
        {'_id': db_item['_id']}, {'$inc': {'order': offset}})
    g.db.todo.items.update(
        {'_id': other_item['_id']}, {'$inc': {'order': -offset}})

@app.route('/move_down', methods=['POST'])
def move_down():
    if not session.get('logged_in'):
        abort(401)

    try:
        reorder('down', request.form['item'])
    except DataError as error:
        return make_response(jsonify({'error': str(error)}), 400)

    return jsonify({'result': True})

@app.route('/move_up', methods=['POST'])
def move_up():
    if not session.get('logged_in'):
        abort(401)

    try:
        reorder('up', request.form['item'])
    except DataError as error:
        return make_response(jsonify({'error': str(error)}), 400)

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
