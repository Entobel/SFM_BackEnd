from abc import ABC, abstractmethod

from application.schemas.produciton_type_schemas import ProductionTypeDTO


class IUpdateProductionTypeUC(ABC):
    @abstractmethod
    def execute(self, production_type_dto: ProductionTypeDTO) -> bool: ...
