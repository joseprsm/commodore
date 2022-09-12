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


class User(BaseModel):

    name: str
    email: str
