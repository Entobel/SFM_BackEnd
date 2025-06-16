from abc import ABC, abstractmethod

from app.domain.entities.packing_type_entity import PackingTypeEntity


class IPackingTypeRepository(ABC):
    @abstractmethod
    def get_list_packing_type(
        self,
        page: int,
        page_size: int,
        search: str,
        is_active: bool,
    ) -> list[PackingTypeEntity]: ...
