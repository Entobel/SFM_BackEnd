from abc import abstractmethod, ABC

from app.domain.entities.antioxidiant_type_entity import AntioxidantTypeEntity


class IAntioxidantTypeRepository(ABC):
    @abstractmethod
    def get_list_antioxidant_types(
        self,
        page: int,
        page_size: int,
        search: str,
        is_active: bool | None,
    ) -> dict[
        "items": list[AntioxidantTypeEntity],
        "total": int,
        "page": int,
        "page_size": int,
        "total_pages": int,
    ]: ...
