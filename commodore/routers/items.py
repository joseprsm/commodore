from fastapi import APIRouter

from commodore.models.item import Item, ItemCategory


router = APIRouter()


@router.post("/{space}/items")
async def create_category(space: str, category: ItemCategory):
    return category.create(space)


@router.get("/{space}/items")
async def get_categories(space: str):
    return {"categories": ItemCategory.list(space)}


@router.put("/{space}/items/{category}")
async def update_category(space: str, category: str, update: dict):
    return ItemCategory.update(space, category, update)


@router.get("/{space}/items/{category}")
async def get_category(space: str, category: str):
    return ItemCategory.get(space, category)


@router.delete("/{space}/items/{category}")
async def delete_category(space: str, category: str):
    ItemCategory.delete(space, category)
    return {"msg": f"Item category {category} deleted"}


@router.post("/{space}/items/{category}")
async def create_item(space: str, category: str, item: Item):
    return item.create(space, category)


@router.get("/{space}/items/{category}/all")
async def get_items(space: str, category: str):
    return Item.list(space, category)


@router.put("/{space}/items/{category}/{item_id}")
async def update_item(space: str, category: str, item_id: str | int, update: dict):
    return Item.update(space, category, item_id, update)


@router.get("/{space}/items/{category}/{item_id}")
async def get_item(space: str, category: str, item_id: int | str):
    return Item.get(space, category, item_id)


@router.delete("/{space}/items/{category}/{item_id}")
async def delete_item(space: str, category: str, item_id: int | str):
    Item.delete(space, category, item_id)
    return {"msg": f"Item {item_id} deleted"}
