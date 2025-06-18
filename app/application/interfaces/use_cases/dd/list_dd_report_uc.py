from abc import ABC, abstractmethod

from typing import TypedDict

from app.domain.entities.dd_entity import DdEntity


class ListDdReportType(TypedDict):
    items: tuple[list[DdEntity], tuple[int, int]]
    total: int
    page: int
    page_size: int
    total_pages: int


class IListDdReportUC(ABC):
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
    ) -> ListDdReportType: ...
