from contextlib import closing
from app import connect_db

DUMMY_DATA = [
    {
    'name': 'grec',
    'progress': .8,
    'link': 'https://github.com/brisad/grec',
    'updates': []
    },

    {
    'name': 'kaimu',
    'progress': .4,
    'link': 'https://github.com/brisad/kaimu',
    'updates': []
    }
]


def init_db():
    with closing(connect_db()) as client:
        for item in DUMMY_DATA:
            client.todo.items.insert(item)
