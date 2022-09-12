from commodore.app.db import db


def get_n_users():
    return db.get().to_dict()['n_users']


def get_n_items():
    return db.get().to_dict()['n_items']
