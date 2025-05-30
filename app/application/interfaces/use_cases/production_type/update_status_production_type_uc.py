from abc import ABC, abstractmethod

from application.dto.produciton_type_dto import ProductionTypeDTO


class IUpdateStatusProductionTypeUC(ABC):
    @abstractmethod
    def execute(self, production_type_dto: ProductionTypeDTO) -> bool: ...
