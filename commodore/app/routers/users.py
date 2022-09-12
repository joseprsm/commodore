import json

from fastapi import APIRouter

from commodore.app.db import db
from commodore.app.models import User
from commodore.app.utils import get_n_users

router = APIRouter()
col_ref = db.collection("users")


@router.get("/users")
async def get_users(name: str = None):
    col = col_ref.where("name", "==", name) if name else col_ref
    documents = col.get()
    return {
        "users": [
            doc.to_dict() for doc in documents
        ]
    }


@router.post("/users")
async def create_user(user: User):
    u = json.loads(user.json())
    user_id = get_n_users() + 1
    col_ref.document(str(user_id)).set(u)
    db.update({"n_users": user_id})
    return u
