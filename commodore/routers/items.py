from fastapi import APIRouter

from commodore.models import Item


router = APIRouter()


@router.post("/{space}/items")
async def create_item(space: str, item: Item):
    return item.create(space)


@router.get("/{space}/items")
async def get_items(
    space: str,
    name: str = None,
    min_price: float = None,
    max_price: float = None,
    recurring: bool = None,
):
    return {"items": Item.get_all(space, name, min_price, max_price, recurring)}


@router.get("/{space}/items/{item_id}")
async def get_item(space: str, item_id: int):
    return Item.get(space, item_id)


@router.put("/{space}/items/{item_id}")
async def update_item(space: str, item_id: int, update: dict):
    return Item.update(space, item_id, update)


@router.delete("/{space}/items/{item_id}")
async def delete_item(space: str, item_id: int):
    Item.delete(space, item_id)
    return {"msg": f"item {item_id} deleted"}
