from app.application.interfaces.use_cases.dd.list_dd_report_uc import IListDdReportUC, ListDdReportType
from app.domain.interfaces.repositories.dd_repository import IDdRepository


class ListDdReportUC(IListDdReportUC):
    def __init__(self, dd_repo: IDdRepository) -> None:
        self.dd_repo = dd_repo

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
    ) -> 'ListDdReportType':
        return self.dd_repo.get_list_dd_report(
            page=page,
            page_size=page_size,
            search=search,
            factory_id=factory_id,
            start_date=start_date,
            end_date=end_date,
            report_status=report_status,
            is_active=is_active,
        )
