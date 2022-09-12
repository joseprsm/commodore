import json

from fastapi import APIRouter

from commodore.app import db
from commodore.app.models import Subscription

router = APIRouter()


@router.post("/{space}/subscriptions")
async def create_subscription(space: str, sub: Subscription):
    s = json.loads(sub.json())
    db.document(space).collection("subscriptions").document().set(s)
    return s
