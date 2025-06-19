from abc import abstractmethod, ABC

from app.domain.entities.dried_larvae_discharge_type_entity import DriedLarvaeDischargeTypeEntity


class IDriedLarvaeDischargeTypeRepository(ABC):
    @abstractmethod
    def get_list_dried_larvae_discharge_types(
        self,
        page: int,
        page_size: int,
        search: str,
        is_active: bool | None,
    ) -> dict[
        "items": list[DriedLarvaeDischargeTypeEntity],
        "total": int,
        "page": int,
        "page_size": int,
        "total_pages": int,
    ]: ...
