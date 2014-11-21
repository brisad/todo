from pymongo import ASCENDING, DESCENDING
from pymongo.errors import PyMongoError


class DataError(Exception):
    pass


def get_all(items):
    return list(items.find().sort('order', ASCENDING))

def add(items, name, progress, description):
    one_sorted_item = list(items.find().sort('order', DESCENDING).limit(1))
    if one_sorted_item:
        order = one_sorted_item[0]['order'] + 1
    else:
        order = 0

    try:
        items.insert({'_id': name, 'progress': progress,
                      'description': description, 'order': order})
    except PyMongoError:
        raise DataError()

def update(items, name, progress, description):
    try:
        items.update({'_id': name}, {'$set': {
            'progress': progress,
            'description': description
            }})
    except PyMongoError:
        raise DataError()

def remove(items, name):
    db_item = items.find_one({'_id': name})
    if db_item is None:
        raise DataError('invalid item')

    order = db_item['order']
    items.remove({'_id': name})
    items.update({'order': {'$gt': order}}, {'$inc': {'order': -1}}, multi=True)

def reorder(items, direction, name):
    db_item = items.find_one({'_id': name})
    if db_item is None:
        raise DataError('invalid item')

    if direction == 'up':
        offset = -1
    else:
        offset = 1

    order = db_item['order']
    other_item = items.find_one({'order': order + offset})

    if other_item is None:
        if direction == 'up':
            raise DataError('first item')
        else:
            raise DataError('last item')

    items.update({'_id': db_item['_id']}, {'$inc': {'order': offset}})
    items.update({'_id': other_item['_id']}, {'$inc': {'order': -offset}})
