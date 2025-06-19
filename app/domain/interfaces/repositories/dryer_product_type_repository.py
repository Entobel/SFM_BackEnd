from abc import abstractmethod, ABC

from app.domain.entities.dryer_product_type_entity import DryerProductTypeEntity


class IDryerProductTypeRepository(ABC):
    @abstractmethod
    def get_list_dryer_product_types(
        self,
        page: int,
        page_size: int,
        search: str,
        is_active: bool | None,
    ) -> dict[
        "items": list[DryerProductTypeEntity],
        "total": int,
        "page": int,
        "page_size": int,
        "total_pages": int,
    ]: ...
