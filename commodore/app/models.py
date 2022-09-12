from datetime import datetime

from pydantic import BaseModel


class Space(BaseModel):

    name: str
    n_users: int = 0
    n_items: int = 0


class Item(BaseModel):

    name: str
    description: str | None
    price: float
    recurring: bool | None
    entrances: int | None


class User(BaseModel):

    name: str
    email: str
    subscription: str | None


class Subscription(BaseModel):

    user_id: int
    item_id: int
    start_date: datetime = datetime.now()
    end_date: datetime | None
