import json

from fastapi import APIRouter

from commodore.app.base import db
from commodore.app.models import Item


router = APIRouter()
col_ref = db.collection("items")


@router.post("/items")
async def create_item(item: Item):
    it = json.loads(item.json())
    col_ref.document().set(it)
    return it


@router.get("/items")
async def get_items(name: str = None, min_price: float = None, max_price: float = None, recurring: bool = None):
    col = col_ref.where("name", "==", name) if name else col_ref
    col = col.where("price", ">=", min_price) if min_price else col
    col = col.where("price", "<=", max_price) if max_price else col
    col = col.where("recurring", "==", recurring) if recurring else col

    documents = col.get()
    return {
        "items": [
            doc.to_dict() for doc in documents
        ]
    }
