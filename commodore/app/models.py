from pydantic import BaseModel


class Item(BaseModel):

    name: str
    description: str | None
    price: float
    recurring: bool | None


class User(BaseModel):

    name: str
    email: str
