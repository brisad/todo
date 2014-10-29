from contextlib import closing
from app import connect_db

DUMMY_DATA = [
    {
    'name': 'grec',
    'description': 'Colorize terminal text with regular expressions.',
    'progress': .8,
    'link': 'https://github.com/brisad/grec',
    'updates': []
    },

    {
    'name': 'kaimu',
    'description': 'Easy file sharing between devices on the same local network.',
    'progress': .4,
    'link': 'https://github.com/brisad/kaimu',
    'updates': []
    }
]


def init_db():
    with closing(connect_db()) as client:
        for item in DUMMY_DATA:
            client.todo.items.insert(item)
