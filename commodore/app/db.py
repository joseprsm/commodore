import os

from google.cloud import firestore

PROJECT_ID: str = os.environ.get("PROJECT_ID")

# noinspection PyTypeChecker, PydanticTypeChecker
client = firestore.Client(project=PROJECT_ID).collection("commodore")
db = client.document("commodore")


if len(client.get()) == 0:
    db.set({
        "n_users": 0,
        "n_items": 0
    })
