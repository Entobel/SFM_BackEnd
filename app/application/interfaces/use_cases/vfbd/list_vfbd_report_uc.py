from abc import ABC, abstractmethod

from typing import TypedDict

from app.domain.entities.vfbd_entity import VfbdEntity


class ListVfbdReportType(TypedDict):
    items: tuple[list[VfbdEntity], tuple[int, int]]
    total: int
    page: int
    page_size: int
    total_pages: int


class IListVfbdReportUC(ABC):
    @abstractmethod
    def execute(
        self,
        page: int,
        page_size: int,
        search: str,
        factory_id: int | None,
        start_date: str | None,
        end_date: str | None,
        report_status: int | None,
        is_active: bool | None,
    ) -> ListVfbdReportType: ...
