from abc import ABC, abstractmethod

from app.domain.entities.production_type_entity import ProductionTypeEntity


class IProductionTypeRepository(ABC):
    @abstractmethod
    def get_all_production_types(
        self,
        page: int,
        page_size: int,
        search: str,
        is_active: bool,
    ) -> dict[
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
        "items" : list[ProductionTypeEntity],
    ]: ...

    @abstractmethod
    def get_production_type_by_name(self, name: str) -> ProductionTypeEntity: ...

    @abstractmethod
    def get_production_type_by_id(self, id: int) -> ProductionTypeEntity: ...

    @abstractmethod
    def create_production_type(
        self, production_type_entity: ProductionTypeEntity
    ) -> bool: ...

    @abstractmethod
    def update_production_type(
        self, production_type_entity: ProductionTypeEntity
    ) -> bool: ...

    @abstractmethod
    def update_status_production_type(
        self, production_type_entity: ProductionTypeEntity
    ) -> bool: ...
