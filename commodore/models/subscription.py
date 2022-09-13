from datetime import datetime

from pydantic import BaseModel

from commodore.models import Plan, User
from commodore.models.base import SpaceResource


class Subscription(BaseModel, SpaceResource):

    user_id: int
    plan_id: int
    start_date: datetime = datetime.now()
    end_date: datetime | None
    active: bool = True
    entrances: int | None

    def create(self, space: str):
        User.id_exists(space, self.user_id)
        Plan.id_exists(space, self.plan_id)

        self.entrances = (
            self.entrances
            if self.entrances
            else self._get_space_document(space)
            .collection("plans")
            .document(str(self.plan_id))
            .get()
            .to_dict()["entrances"]
        )

        doc = self.get_document(space)
        doc.set(self.__dict__)
        User.get_document(space, self.user_id).update({"subscription": doc.id})
        return self

    @classmethod
    def get(cls, space: str, id_: str):
        doc = cls.get_document(space, id_).get().to_dict()
        if doc:
            return Subscription(**doc)
        raise ValueError(f"Subscription {id_} not found!")

    def update(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass

    @classmethod
    def list(cls, space: str):
        docs = cls._get_collection(space).get()
        return [Subscription(**doc.to_dict()) for doc in docs]

    @staticmethod
    def _get_collection_id() -> str:
        return "subscriptions"
