from abc import abstractmethod, ABC

from app.domain.entities.dryer_machine_type_entity import DryerMachineTypeEntity


class IDryerMachineTypeRepository(ABC):
    @abstractmethod
    def get_list_dryer_machine_types(
        self,
        page: int,
        page_size: int,
        search: str,
        is_active: bool | None,
    ) -> dict[
        "items": list[DryerMachineTypeEntity],
        "total": int,
        "page": int,
        "page_size": int,
        "total_pages": int,
    ]: ...
