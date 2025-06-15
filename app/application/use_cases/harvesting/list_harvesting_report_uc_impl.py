from app.application.interfaces.use_cases.harvesting.list_harvesting_report_uc import IListHarvestingReportUC, ListHarvestingReportType
from app.domain.interfaces.repositories.harvesting_repository import IHarvestingRepository


class ListHarvestingReportUC(IListHarvestingReportUC):
    def __init__(self, harvesting_repo: IHarvestingRepository) -> None:
        self.harvesting_repo = harvesting_repo

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
    ) -> ListHarvestingReportType:
        return self.harvesting_repo.get_list_harvesting_report(
            page=page,
            page_size=page_size,
            search=search,
            factory_id=factory_id,
            start_date=start_date,
            end_date=end_date,
            report_status=report_status,
            is_active=is_active,
        )
