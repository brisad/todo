from contextlib import closing
from app import connect_db

DUMMY_DATA = [
    {
    '_id': 'grec',
    'description': '<p>Colorize terminal text with regular expressions.</p>' \
                   '<p><a href="https://github.com/brisad/grec">https://github.com/brisad/grec</a></p>',
    'progress': .8,
    'order': 1
    },

    {
    '_id': 'kaimu',
    'description': '<p>Easy file sharing between devices on the same local network.</p>' \
                   '<p><a href="https://github.com/brisad/kaimu">https://github.com/brisad/kaimu</a></p>',
    'progress': .4,
    'order': 2
    }
]


def init_db():
    with closing(connect_db()) as client:
        for item in DUMMY_DATA:
            client.todo.items.insert(item)
