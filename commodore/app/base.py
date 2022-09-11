import os

from google.cloud import firestore

PROJECT_ID: str = os.environ.get("PROJECT_ID")

# noinspection PyTypeChecker, PydanticTypeChecker
db = firestore.Client(project=PROJECT_ID).collection("commodore").document("commodore")
