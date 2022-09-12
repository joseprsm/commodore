import json

from fastapi import APIRouter

from commodore.app import db
from commodore.app.models import User
from commodore.app.utils import get_n_users, id_exists

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


@router.put("/{space}/users/{user_id}")
async def update_user(space: str, user_id: int, update: dict):
    if not id_exists(space, 'users')(str(user_id)):
        raise ValueError('`user_id` does not exist')
    doc = db.document(space).collection('users').document(str(user_id))
    doc.update(update)
    return doc.get().to_dict()


@router.delete("/{space}/users/{user_id}")
async def delete_user(space: str, user_id: int):
    if not id_exists(space, 'users')(str(user_id)):
        raise ValueError('`user_id` does not exist')
    db.document(space).collection('users').document(str(user_id)).delete()
    n_users = get_n_users(space)
    db.document(space).update({"n_users": n_users - 1})
    return {"msg": f"user {user_id} deleted"}


@router.get("/{space}/users/{user_id}")
async def get_user(space: str, user_id: int):
    if not id_exists(space, 'users')(str(user_id)):
        raise ValueError('`user_id` does not exist')
    return db.document(space).collection('users').document(str(user_id)).get().to_dict()
