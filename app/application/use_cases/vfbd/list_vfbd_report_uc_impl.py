from app.application.interfaces.use_cases.vfbd.list_vfbd_report_uc import IListVfbdReportUC, ListVfbdReportType
from app.domain.interfaces.repositories.vfbd_repository import IVfbdRepository


class ListVfbdReportUC(IListVfbdReportUC):
    def __init__(self, vfbd_repo: IVfbdRepository) -> None:
        self.vfbd_repo = vfbd_repo

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
    ) -> 'ListVfbdReportType':
        return self.vfbd_repo.get_list_vfbd_report(
            page=page,
            page_size=page_size,
            search=search,
            factory_id=factory_id,
            start_date=start_date,
            end_date=end_date,
            report_status=report_status,
            is_active=is_active,
        )
