from flask import Flask, render_template, redirect, request, url_for
from flask import g, session, flash, jsonify, make_response, abort
from pymongo import MongoClient
import model

app = Flask(__name__)
app.config.from_pyfile('config.py')

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
    items = model.get_all(g.db.todo.items)
    return render_template('index.html', items=items)

# Not reached with an AJAX request
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

    try:
        model.add(g.db.todo.items,
                  request.form['name'], progress, request.form['description'])
    except model.DataError:
        flash("Failed to add item")
        return redirect(url_for('root'))

    return redirect(url_for('root'))

@app.route('/remove', methods=['POST'])
def remove_item():
    if not session.get('logged_in'):
        abort(401)

    try:
        model.remove(g.db.todo.items, request.form['item'])
    except model.DataError as error:
        return make_response(jsonify({'error': str(error)}), 400)

    return jsonify({'result': True})

# Not reached with an AJAX request
@app.route('/edit', methods=['POST'])
def edit_item():
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

    try:
        model.update(g.db.todo.items,
                     request.form['name'], progress, request.form['description'])
    except model.DataError:
        flash("Failed to update item")
        return redirect(url_for('root'))

    return redirect(url_for('root'))

@app.route('/move_down', methods=['POST'])
def move_down():
    if not session.get('logged_in'):
        abort(401)

    try:
        model.reorder(g.db.todo.items, 'down', request.form['item'])
    except model.DataError as error:
        return make_response(jsonify({'error': str(error)}), 400)

    return jsonify({'result': True})

@app.route('/move_up', methods=['POST'])
def move_up():
    if not session.get('logged_in'):
        abort(401)

    try:
        model.reorder(g.db.todo.items, 'up', request.form['item'])
    except model.DataError as error:
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
