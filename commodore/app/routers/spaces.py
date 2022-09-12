import json

from fastapi import APIRouter

from commodore.app import db
from commodore.app.models import Space


router = APIRouter()


@router.post("/spaces")
async def create_space(space: Space):
    space = json.loads(space.json())
    db.document(parse_name(space["name"])).set(space)
    return space


def parse_name(name: str):
    return name.replace(" ", "").lower()
