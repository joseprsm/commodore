import json

from fastapi import APIRouter

from commodore import db
from commodore.models import Subscription
from commodore.utils import id_exists


router = APIRouter()


@router.post("/{space}/subscriptions")
async def create_subscription(space: str, sub: Subscription):
    s = json.loads(sub.json())

    if not id_exists(space, "items")(s["item_id"]):
        raise ValueError("`item_id` does not exist")

    if not id_exists(space, "users")(s["user_id"]):
        raise ValueError("`user_id` does not exist")

    s["entrances"] = (
        db.document(space)
        .collection("items")
        .document(str(s["item_id"]))
        .get()
        .to_dict()["entrances"]
    )
    sub_doc = db.document(space).collection("subscriptions").document()
    sub_doc.set(s)

    db.document(space).collection("users").document(str(s["user_id"])).update(
        {"subscription": sub_doc.id}
    )
    return s


@router.get("/{space}/subscriptions")
def get_subscriptions(space: str):
    documents = db.document(space).collection("subscriptions").get()
    return {"subscriptions": [doc.to_dict() for doc in documents]}
