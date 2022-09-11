import json

from fastapi import APIRouter

from commodore.app.base import db
from commodore.app.models import User


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
    col_ref.document().set(u)
    return u
