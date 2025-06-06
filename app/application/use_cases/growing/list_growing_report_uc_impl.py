from app.application.interfaces.use_cases.growing.list_growing_report_uc import (
    IListGrowingReportUC,
    ListGrowimgReportType,
)

from app.domain.interfaces.repositories.growing_repository import IGrowingRepository


class ListGrowingReportUC(IListGrowingReportUC):
    def __init__(self, growing_repo: IGrowingRepository) -> None:
        self.growing_repo = growing_repo

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
    ) -> ListGrowimgReportType:
        return self.growing_repo.get_list_growing_report(
            page=page,
            page_size=page_size,
            diet_id=diet_id,
            search=search,
            production_object_id=production_object_id,
            production_type_id=production_type_id,
            factory_id=factory_id,
            start_date=start_date,
            end_date=end_date,
            substrate_moisture_lower_bound=substrate_moisture_lower_bound,
            substrate_moisture_upper_bound=substrate_moisture_upper_bound,
            report_status=report_status,
            is_active=is_active,
        )
