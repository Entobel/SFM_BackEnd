from domain.entities.production_object_entity import ProductionObjectEntity
from abc import ABC, abstractmethod


class IListProductionObjectUC(ABC):
    @abstractmethod
    def execute(
        self,
        page: int,
        page_size: int,
        search: str,
        is_active: bool,
    ) -> dict[
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
        "items" : list[ProductionObjectEntity],
    ]: ...
