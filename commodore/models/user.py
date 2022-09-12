from pydantic import BaseModel

from commodore.models.base import IdentifiableMixin


class User(BaseModel, IdentifiableMixin):

    name: str
    email: str
    subscription: str | None

    def create(self, space):
        user_id = self.cardinality(space) + 1
        self.get_document(space, user_id).set(self.__dict__)
        self._get_space_document(space).update({"n_users": user_id})
        return self

    @classmethod
    def get(cls, space: str, user_id: int):
        cls.id_exists(space, user_id)
        return User(**cls.get_document(space, user_id).get().to_dict())

    @classmethod
    def update(cls, space: str, user_id: int, update: dict):
        cls.id_exists(space, user_id)
        doc = cls.get_document(space, user_id)
        doc.update(update)
        return User(**doc.get().to_dict())

    @classmethod
    def delete(cls, space: str, user_id: int):
        cls.id_exists(space, user_id)
        cls.get_document(space, user_id).delete()
        n_users = cls.cardinality(space)
        cls._get_space_document(space).update({"n_users": n_users - 1})

    @classmethod
    def get_all(cls, space: str, name: str = None):
        col = cls._get_collection(space)
        col = col.where("name", "==", name) if name else col
        return [User(**doc.to_dict()) for doc in col.get()]

    @staticmethod
    def _get_collection_id() -> str:
        return "users"