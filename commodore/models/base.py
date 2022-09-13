from abc import ABC, abstractmethod

from google.cloud import firestore

from commodore import db


class BaseInterface:
    @abstractmethod
    def create(self, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def get(cls, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def update(cls, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def delete(cls, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def list(cls, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def _get_document(cls, **kwargs):
        pass


class SpaceResource(BaseInterface, ABC):
    @staticmethod
    def _get_space_document(space):
        return db.document(space)

    @classmethod
    def _get_collection(cls, space) -> firestore.CollectionReference:
        collection_id = cls._get_collection_id()
        return cls._get_space_document(space).collection(collection_id)

    @classmethod
    def _get_document(cls, space: str, id_: str | int | None = None, **kwargs):
        col = cls._get_collection(space)
        doc = col.document(str(id_)) if id_ else col.document()
        return doc

    @staticmethod
    @abstractmethod
    def _get_collection_id() -> str:
        pass


class IdentifiableMixin(SpaceResource, ABC):
    @classmethod
    def cardinality(cls, space: str) -> int:
        return db.document(space).get().to_dict()[f"n_{cls._get_collection_id()}"]

    @classmethod
    def id_exists(cls, space: str, value: str | int):
        if cls._get_document(space, value).get().to_dict() is None:
            raise ValueError(f"ID {value} does not exist")
        return True
