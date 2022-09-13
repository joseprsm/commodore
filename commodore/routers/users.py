from fastapi import APIRouter

from commodore.models import User


router = APIRouter()


@router.get("/{space}/users")
async def get_users(space: str, name: str = None):
    return {"users": User.list(space, name)}


@router.post("/{space}/users")
async def create_user(space: str, user: User):
    return user.create(space)


@router.put("/{space}/users/{user_id}")
async def update_user(space: str, user_id: int, update: dict):
    return User.update(space, user_id, update)


@router.delete("/{space}/users/{user_id}")
async def delete_user(space: str, user_id: int):
    User.delete(space, user_id)
    return {"msg": f"user {user_id} deleted"}


@router.get("/{space}/users/{user_id}")
async def get_user(space: str, user_id: int):
    return User.get(space, user_id)
