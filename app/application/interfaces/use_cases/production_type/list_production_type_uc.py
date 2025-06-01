from abc import ABC, abstractmethod

from app.domain.entities.production_type_entity import ProductionTypeEntity


class IListProductionTypeUC(ABC):
    @abstractmethod
    def execute(self, page: int,
        page_size: int,
        search: str,
        is_active: bool,) -> list[ProductionTypeEntity]: ...
