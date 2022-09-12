import json

from fastapi import APIRouter

from commodore.app import db
from commodore.app.utils import id_exists
from commodore.app.models import Subscription

router = APIRouter()


@router.post("/{space}/subscriptions")
async def create_subscription(space: str, sub: Subscription):
    s = json.loads(sub.json())

    if not id_exists(space, 'items')(s['item_id']):
        raise ValueError('`item_id` does not exist')

    if not id_exists(space, 'users')(s['user_id']):
        raise ValueError('`user_id` does not exist')

    s['entrances'] = db.document(space).collection('items').document(str(s['item_id'])).get().to_dict()['entrances']
    db.document(space).collection("subscriptions").document().set(s)
    return s
