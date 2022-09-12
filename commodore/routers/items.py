import json

from fastapi import APIRouter

from commodore import db
from commodore.models import Item
from commodore.utils import get_n_items, id_exists


router = APIRouter()


@router.post("/{space}/items")
async def create_item(space: str, item: Item):
    it = json.loads(item.json())
    item_id = get_n_items(space) + 1
    db.document(space).collection("items").document(str(item_id)).set(it)
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
    col_ref = db.document(space).collection("items")

    col = col_ref.where("name", "==", name) if name else col_ref
    col = col.where("price", ">=", min_price) if min_price else col
    col = col.where("price", "<=", max_price) if max_price else col
    col = col.where("recurring", "==", recurring) if recurring else col

    documents = col.get()
    return {"items": [doc.to_dict() for doc in documents]}


@router.get("/{space}/items/{item_id}")
async def get_item(space: str, item_id: int):
    if not id_exists(space, "items")(str(item_id)):
        raise ValueError("`item_id` does not exist")
    return db.document(space).collection("items").document(str(item_id)).get().to_dict()


@router.put("/{space}/items/{item_id}")
async def update_item(space: str, item_id: int, update: dict):
    if not id_exists(space, "items")(str(item_id)):
        raise ValueError("`item_id` does not exist")
    doc = db.document(space).collection("items").document(str(item_id))
    doc.update(update)
    return doc.get().to_dict()


@router.delete("/{space}/items/{item_id}")
async def delete_item(space: str, item_id: int):
    if not id_exists(space, "items")(str(item_id)):
        raise ValueError("`item_id` does not exist")
    db.document(space).collection("items").document(str(item_id)).delete()
    n_items = get_n_items(space)
    db.document(space).update({"n_items": n_items - 1})
    return {"msg": f"item {item_id} deleted"}
