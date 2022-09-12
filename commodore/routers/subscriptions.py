from fastapi import APIRouter

from commodore.models.subscription import Subscription


router = APIRouter()


@router.post("/{space}/subscriptions")
async def create_subscription(space: str, sub: Subscription):
    sub = sub.create(space)
    return sub


@router.get("/{space}/subscriptions")
def get_subscriptions(space: str):
    return {"subscriptions": Subscription.get_all(space)}


@router.get("/{space}/subscriptions/{sub_id}")
def get_subscription(space: str, sub_id: str):
    return Subscription.get(space, sub_id)
