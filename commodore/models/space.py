from pydantic import BaseModel

from commodore import db
from commodore.models.base import BaseInterface


class Space(BaseModel, BaseInterface):

    name: str
    capacity: int
    n_users: int = 0
    n_plans: int = 0

    def create(self):
        self._get_document(self._parse_name(self.name)).set(self.__dict__)
        return self

    @classmethod
    def get(cls, name: str):
        return Space(**cls._get_document(name).get().to_dict())

    @classmethod
    def update(cls, name: str, update: dict):
        doc = cls._get_document(name)
        doc.update(update)
        return Space(**doc.get().to_dict())

    @classmethod
    def delete(cls, name: str):
        cls._get_document(name).delete()

    @classmethod
    def list(cls, **kwargs):
        return [Space(**doc.to_dict()) for doc in db.get()]

    @staticmethod
    def _parse_name(name: str):
        return name.replace(" ", "").lower()

    @classmethod
    def _get_document(cls, name: str):
        return db.document(name)
