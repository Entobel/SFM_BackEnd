from domain.entities.production_object_entity import ProductionObjectEntity
from abc import ABC, abstractmethod


class IListProductionObjectUC(ABC):
    @abstractmethod
    def execute(self) -> list[ProductionObjectEntity]: ...
