from commodore.app import db


def get_n_users(space):
    return db.document(space).get().to_dict()["n_users"]


def get_n_items(space):
    return db.document(space).get().to_dict()["n_items"]



def get_n_items():
    return db.get().to_dict()['n_items']
