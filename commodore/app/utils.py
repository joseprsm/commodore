from commodore.app import db


def get_n_users(space):
    return db.document(space).get().to_dict()["n_users"]


def get_n_items(space):
    return db.document(space).get().to_dict()["n_items"]


def id_exists(collection_id: str, value: str | int):
    return db.collection(collection_id).document(str(value)).get().to_dict() is not None


def get_entrance_passes():
    return [
        doc.id
        for doc in db.collection("items").where("recurring", "!=", "true").stream()
    ]
