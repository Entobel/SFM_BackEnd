from abc import ABC, abstractmethod

from app.domain.entities.product_type_entity import ProductTypeEntity


class IListProductTypeUC(ABC):
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
        "items": list[ProductTypeEntity],
    ]: ...
