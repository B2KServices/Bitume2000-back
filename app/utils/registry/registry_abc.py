import abc
from typing import Generic, TypeVar

InstanceType = TypeVar('InstanceType')


class RegistryABC(abc.ABC, Generic[InstanceType]):
    """
    Abstract base class defining methods for interacting with a registry of instances,
    with error handling using custom exceptions.

    Attributes
    ----------
    InstanceType : type
        Generic type variable representing the type of instances handled by the registry.
    """

    @abc.abstractmethod
    def create_one(self, instance: InstanceType) -> InstanceType: ...

    @abc.abstractmethod
    def delete_one_or_fail(self, instance: InstanceType): ...

    @abc.abstractmethod
    def delete_one_by_id_or_fail(self, id_instance: str): ...

    @abc.abstractmethod
    def get_one_by_id(self, id_instance: str) -> InstanceType | None: ...

    @abc.abstractmethod
    def get_one_by_id_or_fail(self, id_instance: str) -> InstanceType: ...

    @abc.abstractmethod
    def get_all(self) -> list[InstanceType]: ...

    @abc.abstractmethod
    def get_all_where(self, **kwargs) -> list[InstanceType]: ...

    @abc.abstractmethod
    def get_one_or_fail_where(self, **kwargs) -> InstanceType: ...
