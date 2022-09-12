from commodore.app import db


def get_n_users(space):
    return db.document(space).get().to_dict()["n_users"]


def get_n_items(space):
    return db.document(space).get().to_dict()["n_items"]


def id_exists(space: str, collection_id: str):
    def check(value: str | int):
        return db.document(space).collection(collection_id).document(str(value)).get().to_dict() is not None
    return check


def get_entrance_passes():
    return [
        doc.id
        for doc in db.collection("items").where("recurring", "!=", "true").stream()
    ]
