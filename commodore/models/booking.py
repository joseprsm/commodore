from datetime import datetime

from pydantic import BaseModel

from commodore.models.base import SpaceResource


class Booking(BaseModel, SpaceResource):

    user_id: int
    item_category: str
    item_id: int
    start: datetime = datetime.now()
    end: datetime | None

    def create(self, space: str):
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
