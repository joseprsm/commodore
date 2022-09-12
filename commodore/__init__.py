import os
import warnings

from google.cloud import firestore


__version__ = "0.1.0"

PROJECT_ID: str = os.environ.get("PROJECT_ID")

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    db = firestore.Client(project=PROJECT_ID).collection("commodore")
