from abc import ABC, abstractmethod

from domain.entities.production_object_entity import ProductionObjectEntity


class IProductionRepository(ABC):
    @abstractmethod
    def get_all_production_objects(self) -> list[ProductionObjectEntity]: ...
