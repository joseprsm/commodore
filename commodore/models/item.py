from pydantic import BaseModel

from commodore import db
from commodore.models.base import BaseInterface, SpaceResource
from commodore.utils import parse_name


_COLLECTION_ID = "items"


class ItemCategory(BaseModel, SpaceResource):

    name: str
    units: int = 1

    def create(self, space):
        self._get_document(space, parse_name(self.name, sep="-")).set(self.__dict__)
        return self

    @classmethod
    def get(cls, space: str, name: str):
        return ItemCategory(**cls._get_document(space, name).get().to_dict())

    @classmethod
    def update(cls, space: str, name: str, update: dict):
        doc = cls._get_document(space, name)
        doc.update(update)
        return ItemCategory(**doc.get().to_dict())

    @classmethod
    def delete(cls, space: str, name: str):
        cls._get_document(space, name).delete()

    @classmethod
    def list(cls, space: str):
        return [
            ItemCategory(**doc.to_dict()) for doc in cls._get_collection(space).get()
        ]

    @staticmethod
    def _get_collection_id() -> str:
        return _COLLECTION_ID


class Item(BaseModel, BaseInterface):

    id: int | str | None

    def create(self, space: str, category: str):
        data = self.__dict__
        doc = self._get_document(space, category, self.id)
        if self.id is None:
            data["id"] = doc.id
        doc.set(data)
        return self

    @classmethod
    def get(cls, space: str, category: str, id_: str | int | None = None):
        cls.id_exists(space, category, id_)
        return Item(**cls._get_document(space, category, id_).get().to_dict())

    @classmethod
    def update(cls, space: str, category: str, id_: str | int, update: dict):
        cls.id_exists(space, category, id_)
        doc = cls._get_document(space, category, id_)
        doc.update(update)
        return Item(**doc.get().to_dict())

    @classmethod
    def delete(cls, space: str, category: str, id_: str | int):
        cls.id_exists(space, category, id_)
        cls._get_document(space, category, id_).delete()

    @classmethod
    def list(cls, space: str, category: str):
        col = cls._get_collection(space, category)
        return [Item(**doc.to_dict()) for doc in col.get()]

    @staticmethod
    def _get_collection(space: str, category: str):
        return (
            db.document(space)
            .collection(_COLLECTION_ID)
            .document(category)
            .collection("units")
        )

    @classmethod
    def _get_document(cls, space: str, category: str, id_: str | int | None):
        col = cls._get_collection(space, category)
        return col.document(str(id_)) if id_ else col.document()

    @classmethod
    def id_exists(cls, space, category, id_):
        if cls._get_document(space, category, id_).get().to_dict() is None:
            raise ValueError(f"ID {id_} does not exist")
        return True
