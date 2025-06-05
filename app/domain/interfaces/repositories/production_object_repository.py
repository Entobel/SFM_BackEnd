from abc import ABC, abstractmethod

from app.domain.entities.production_object_entity import ProductionObjectEntity


class IProductionObjectRepository(ABC):
    @abstractmethod
    def get_all_production_objects(self) -> list[ProductionObjectEntity]: ...

    @abstractmethod
    def get_production_object_by_id(
        self, production_object_entity: ProductionObjectEntity
    ) -> ProductionObjectEntity | None: ...

    @abstractmethod
    def get_production_object_by_name(
        self, name: str
    ) -> ProductionObjectEntity | None: ...

    @abstractmethod
    def create_production_object(
        self, production_object_entity: ProductionObjectEntity
    ) -> bool: ...

    @abstractmethod
    def update_production_object(
        self, production_object_entity: ProductionObjectEntity
    ) -> bool: ...

    @abstractmethod
    def update_status_production_object(
        self, production_object_entity: ProductionObjectEntity
    ) -> bool: ...
