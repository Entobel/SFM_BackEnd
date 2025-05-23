from abc import ABC, abstractmethod

from application.schemas.production_object_schemas import ProductionObjectDTO


class ICreateProductionObjectUC(ABC):
    @abstractmethod
    def execute(self, production_object_dto: ProductionObjectDTO) -> bool: ...
