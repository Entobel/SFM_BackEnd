from abc import ABC, abstractmethod

from app.application.dto.produciton_type_dto import ProductionTypeDTO


class IUpdateStatusProductionTypeUC(ABC):
    @abstractmethod
    def execute(self, production_type_dto: ProductionTypeDTO) -> bool: ...
