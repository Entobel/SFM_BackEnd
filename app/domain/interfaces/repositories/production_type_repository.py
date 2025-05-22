from abc import ABC, abstractmethod

from domain.entities.production_type_entity import ProductionTypeEntity


class IProductionTypeRepository(ABC):
    @abstractmethod
    def get_all_production_types(self) -> list[ProductionTypeEntity]: ...
