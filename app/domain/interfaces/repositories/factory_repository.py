from abc import ABC, abstractmethod
from typing import Optional
from domain.entities.factory_entity import FactoryEntity


class IFactoryRepository(ABC):
    @abstractmethod
    def get_factory_by_id(self, factory_id: int) -> FactoryEntity | None: ...
    @abstractmethod
    def get_list_factory(
        self, page: int, page_size: int, search: str, is_active: Optional[bool] = None
    ) -> list[FactoryEntity]: ...

    @abstractmethod
    def get_factory_by_name(self, name: str) -> FactoryEntity | None: ...

    @abstractmethod
    def create_factory(self, factory: FactoryEntity) -> bool: ...

    @abstractmethod
    def update_factory(self, factory: FactoryEntity) -> bool: ...

    @abstractmethod
    def update_status_factory(self, factory_id: int, is_active: bool) -> bool: ...

    @abstractmethod
    def check_factory_is_used(self, factory_id: int) -> bool: ...
