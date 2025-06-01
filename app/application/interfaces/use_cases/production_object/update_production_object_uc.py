from abc import ABC, abstractmethod

from app.application.dto.production_object_dto import ProductionObjectDTO


class IUpdateProductionObjectUC(ABC):
    @abstractmethod
    def execute(self, production_object_dto: ProductionObjectDTO) -> bool: ...
