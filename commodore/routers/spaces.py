import json

from fastapi import APIRouter

from commodore import db
from commodore.models import Space


router = APIRouter()


@router.get("/spaces")
async def get_spaces():
    documents = db.get()
    return {"spaces": [doc.to_dict() for doc in documents]}


@router.post("/spaces")
async def create_space(space: Space):
    space = json.loads(space.json())
    db.document(parse_name(space["name"])).set(space)
    return space


@router.get("/{space}")
async def get_space(space):
    return db.document(space).get().to_dict()


@router.put("/{space}")
async def update_space(space, update: dict):
    doc = db.document(space)
    doc.update(update)
    return doc.get().to_dict()


@router.delete("/{space}")
async def delete_space(space):
    db.document(space).delete()
    return {"msg": f"Space {space} deleted"}


def parse_name(name: str):
    return name.replace(" ", "").lower()
