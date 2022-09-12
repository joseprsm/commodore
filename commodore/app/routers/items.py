import json

from fastapi import APIRouter

from commodore.app import db
from commodore.app.models import Item
from commodore.app.utils import get_n_items

router = APIRouter()


@router.post("/{space}/items")
async def create_item(space: str, item: Item):
    it = json.loads(item.json())
    item_id = get_n_items(space) + 1
    db.document(space).collection('items').document(str(item_id)).set(it)
    db.document(space).update({"n_items": item_id})
    return it


@router.get("/{space}/items")
async def get_items(
    space: str,
    name: str = None,
    min_price: float = None,
    max_price: float = None,
    recurring: bool = None,
):
    col_ref = db.document(space).collection('items')

    col = col_ref.where("name", "==", name) if name else col_ref
    col = col.where("price", ">=", min_price) if min_price else col
    col = col.where("price", "<=", max_price) if max_price else col
    col = col.where("recurring", "==", recurring) if recurring else col

    documents = col.get()
    return {"items": [doc.to_dict() for doc in documents]}
