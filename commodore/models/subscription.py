from datetime import datetime

from pydantic import BaseModel

from commodore.models import Plan, User
from commodore.models.base import SpaceResource


class Subscription(BaseModel, SpaceResource):

    user_id: int
    plan_id: int | None
    start_date: datetime = datetime.now()
    end_date: datetime | None
    active: bool = True
    plan: Plan | None

    def create(self, space: str):
        User.id_exists(space, self.user_id)

        if self.plan_id is None:
            raise ValueError("Missing plan ID")
        Plan.id_exists(space, self.plan_id)

        doc = self._get_document(space)
        data = self.__dict__
        data["plan"] = Plan.get(space, self.plan_id).__dict__
        data["plan"]["items"] = [it.__dict__ for it in data["plan"]["items"]]
        data["plan"]["id"] = data.pop("plan_id")

        doc.set(self.__dict__)
        User._get_document(space, self.user_id).update({"subscription": doc.id})
        return self

    @classmethod
    def get(cls, space: str, id_: str):
        doc = cls._get_document(space, id_).get().to_dict()
        if doc:
            return Subscription(**doc)
        raise ValueError(f"Subscription {id_} not found!")

    @classmethod
    def update(cls, space: str, id_: str, update: dict):
        doc = cls._get_document(space, id_)
        doc.update(update)
        return Subscription(**doc.get().to_dict())

    @classmethod
    def delete(cls, space: str, id_: str):
        cls._get_document(space, id_).delete()

    @classmethod
    def list(cls, space: str):
        docs = cls._get_collection(space).get()
        return [Subscription(**doc.to_dict()) for doc in docs]

    @staticmethod
    def _get_collection_id() -> str:
        return "subscriptions"
