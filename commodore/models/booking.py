from datetime import datetime

from pydantic import BaseModel

from commodore.models import User
from commodore.models.base import SpaceResource
from commodore.models.subscription import Subscription


class Booking(BaseModel, SpaceResource):

    user_id: int
    item_category: str
    item_id: int | None
    start: datetime = datetime.now()
    end: datetime | None

    def create(self, space: str):
        sub_id = User.get(space, self.user_id).subscription
        sub = Subscription.get(space, sub_id)

        if self.item_category not in [it.name for it in sub.plan.items]:
            raise ValueError("Item category not in user plan")

        for it in sub.plan.items:
            if it.name == self.item_category:
                if it.units == 0:
                    raise ValueError("Plan has no more units for this item category")
                it.units -= 1

        update_sub = dict()
        update_sub["plan"] = sub.plan.__dict__
        update_sub["plan"]["items"] = [it.__dict__ for it in sub.plan.items]
        Subscription.update(space, sub_id, update_sub)

        self._get_document(space).set(self.__dict__)
        return self

    @classmethod
    def get(cls, space: str, booking_id: str):
        return Booking(**cls._get_document(space, booking_id).get().to_dict())

    @classmethod
    def update(cls, space: str, booking_id: str, update: dict):
        doc = cls._get_document(space, booking_id)
        doc.update(update)
        return Booking(**doc.get().to_dict())

    @classmethod
    def delete(cls, space: str, booking_id: str):
        cls._get_document(space, booking_id).delete()

    @classmethod
    def list(cls, space: str):
        col = cls._get_collection(space)
        return [Booking(**doc.to_dict()) for doc in col.get()]

    @staticmethod
    def _get_collection_id() -> str:
        return "bookings"
