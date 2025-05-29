from abc import ABC, abstractmethod

from application.schemas.produciton_type_dto import ProductionTypeDTO


class ICreateProductionTypeUC(ABC):
    @abstractmethod
    def execute(self, production_type_dto: ProductionTypeDTO) -> bool: ...
