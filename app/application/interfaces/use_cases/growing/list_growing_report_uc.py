from abc import ABC, abstractmethod


class IListGrowingReportUC(ABC):
    @abstractmethod
    def execute(
        self,
        page: int,
        page_size: int,
        search: str,
        production_object_id: int | None,
        production_type_id: int | None,
        diet_id: int | None,
        factory_id: int | None,
        start_date: str | None,
        end_date: str | None,
        substrate_moisture_lower_bound: float | None,
        substrate_moisture_upper_bound: float | None,
        report_status: int | None,
        is_active: bool | None,
    ): ...
