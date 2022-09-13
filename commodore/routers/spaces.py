from fastapi import APIRouter

from commodore.models import Space


router = APIRouter()


@router.get("/spaces")
async def get_spaces():
    return {"spaces": Space.list()}


@router.post("/spaces")
async def create_space(space: Space):
    return space.create()


@router.get("/{space}")
async def get_space(space):
    return Space.get(space)


@router.put("/{space}")
async def update_space(space, update: dict):
    return Space.update(space, update)


@router.delete("/{space}")
async def delete_space(space):
    Space.delete(space)
    return {"msg": f"Space {space} deleted"}
