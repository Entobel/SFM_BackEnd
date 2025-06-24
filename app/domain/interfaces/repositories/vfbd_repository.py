from abc import ABC, abstractmethod

from app.domain.entities.vfbd_entity import VfbdEntity


class IVfbdRepository(ABC):
    @abstractmethod
    def get_vfbd_report_by_id(self, vfbd_entity: VfbdEntity) -> VfbdEntity | None: ...

    @abstractmethod
    def get_list_vfbd_report(
        self,
        page: int,
        page_size: int,
        search: str,
        factory_id: int | None,
        start_date: str | None,
        end_date: str | None,
        report_status: int | None,
        is_active: bool | None,
    ) -> dict[
        "items" : list[VfbdEntity],
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
    ]: ...

    @abstractmethod
    def create_vfbd_report(self, vfbd_entity: VfbdEntity) -> bool: ...

    @abstractmethod
    def update_vfbd_report(self, vfbd_entity: VfbdEntity) -> bool: ...
