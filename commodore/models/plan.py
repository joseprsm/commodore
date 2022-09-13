from pydantic import BaseModel

from commodore.models.base import IdentifiableMixin


class PlanItems(BaseModel):

    name: str
    units: int


class Plan(BaseModel, IdentifiableMixin):

    name: str
    price: float
    description: str | None
    recurring: bool | None
    uses: int | None
    items: list[PlanItems] | None

    def create(self, space):
        plan_id = self.cardinality(space) + 1
        doc = self.__dict__
        doc["items"] = [it.__dict__ for it in self.items]
        self._get_document(space, plan_id).set(doc)
        self._get_space_document(space).update({"n_plans": plan_id})
        return self

    @classmethod
    def get(cls, space: str, plan_id: str | int):
        cls.id_exists(space, plan_id)
        return Plan(**cls._get_document(space, plan_id).get().to_dict())

    @classmethod
    def update(cls, space: str, plan_id: str | int, update: dict):
        cls.id_exists(space, plan_id)
        doc = cls._get_document(space, plan_id)
        doc.update(update)
        return Plan(**doc.get().to_dict())

    @classmethod
    def delete(cls, space: str, plan_id: str | int):
        cls.id_exists(space, plan_id)
        cls._get_document(space, plan_id).delete()

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
