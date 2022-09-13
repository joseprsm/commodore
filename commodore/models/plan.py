from pydantic import BaseModel

from commodore.models.base import IdentifiableMixin


class Plan(BaseModel, IdentifiableMixin):

    name: str
    price: float
    description: str | None
    recurring: bool | None
    entrances: int | None

    def create(self, space):
        plan_id = self.cardinality(space) + 1
        self.get_document(space, plan_id).set(self.__dict__)
        self._get_space_document(space).update({"n_plans": plan_id})
        return self

    @classmethod
    def get(cls, space: str, plan_id: str | int):
        cls.id_exists(space, plan_id)
        return Plan(**cls.get_document(space, plan_id).get().to_dict())

    @classmethod
    def update(cls, space: str, plan_id: str | int, update: dict):
        cls.id_exists(space, plan_id)
        doc = cls.get_document(space, plan_id)
        doc.update(update)
        return Plan(**doc.get().to_dict())

    @classmethod
    def delete(cls, space: str, plan_id: str | int):
        cls.id_exists(space, plan_id)
        cls.get_document(space, plan_id).delete()

    @classmethod
    def list(
        cls,
        space: str,
        name: str = None,
        min_price: float = None,
        max_price: float = None,
        recurring: bool = None,
    ):
        col = cls._get_collection(space)
        col = col.where("name", "==", name) if name else col
        col = col.where("price", ">=", min_price) if min_price else col
        col = col.where("price", "<=", max_price) if max_price else col
        col = col.where("recurring", "==", recurring) if recurring else col
        return [Plan(**doc.to_dict()) for doc in col.get()]

    @staticmethod
    def _get_collection_id() -> str:
        return "plans"
