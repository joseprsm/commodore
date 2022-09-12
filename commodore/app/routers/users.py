import json

from fastapi import APIRouter

from commodore.app import db
from commodore.app.models import User
from commodore.app.utils import get_n_users


router = APIRouter()


@router.get("/{space}/users")
async def get_users(space: str, name: str = None):
    col_ref = db.document(space).collection("users")
    col = col_ref.where("name", "==", name) if name else col_ref
    documents = col.get()
    return {"users": [doc.to_dict() for doc in documents]}


@router.post("/{space}/users")
async def create_user(space: str, user: User):
    u = json.loads(user.json())
    user_id = get_n_users(space) + 1
    db.document(space).collection("users").document(str(user_id)).set(u)
    db.document(space).update({"n_users": user_id})
    return u
