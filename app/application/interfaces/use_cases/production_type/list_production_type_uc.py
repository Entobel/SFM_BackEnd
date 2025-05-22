from abc import ABC, abstractmethod

from domain.entities.production_type_entity import ProductionTypeEntity


class IListProductionTypeUC(ABC):
    @abstractmethod
    def execute(self) -> list[ProductionTypeEntity]: ...
