from abc import ABC, abstractmethod

from application.dto.production_object_dto import ProductionObjectDTO


class ICreateProductionObjectUC(ABC):
    @abstractmethod
    def execute(self, production_object_dto: ProductionObjectDTO) -> bool: ...
