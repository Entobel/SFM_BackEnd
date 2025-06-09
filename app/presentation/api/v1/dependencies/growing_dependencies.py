from fastapi import Depends
from typing import Annotated

from app.application.interfaces.use_cases.growing.create_growing_report_uc import (
    ICreateGrowingReportUC,
)
from app.application.interfaces.use_cases.growing.list_growing_report_uc import (
    IListGrowingReportUC,
)
from app.application.interfaces.use_cases.growing.update_status_growing_report_uc import (
    IUpdateStatusGrowingReportUC,
)
from app.application.use_cases.growing.create_growing_report_uc_impl import (
    CreateGrowingReportUC,
)
from app.application.use_cases.growing.list_growing_report_uc_impl import (
    ListGrowingReportUC,
)
from app.application.use_cases.growing.update_status_growing_report_uc_imply import (
    UpdateStatusGrowingReportUC,
)
from app.domain.interfaces.repositories.growing_repository import IGrowingRepository
from app.infrastructure.database.repositories.growing_repository_impl import (
    GrowingRepository,
)
from app.presentation.api.v1.dependencies.common_dependencies import (
    DatabaseDep,
    QueryHelperDep,
    CommonRepositoryDep,
)

from app.presentation.api.v1.dependencies.zone_dependencies import ZoneRepositoryDep


def get_growing_repository(
    db: DatabaseDep, query_helper: QueryHelperDep
) -> IGrowingRepository:
    return GrowingRepository(conn=db, query_helper=query_helper)


GrowingRepositoryDep = Annotated[IGrowingRepository, Depends(get_growing_repository)]


def get_create_growing_report_uc(
    growing_repo: GrowingRepositoryDep,
    zone_repo: ZoneRepositoryDep,
    common_repo: CommonRepositoryDep,
    query_helper: QueryHelperDep,
) -> ICreateGrowingReportUC:
    return CreateGrowingReportUC(
        growing_repo=growing_repo,
        zone_repo=zone_repo,
        query_helper=query_helper,
        common_repo=common_repo,
    )


def get_list_growing_report_uc(
    growing_repo: GrowingRepositoryDep,
) -> IListGrowingReportUC:
    return ListGrowingReportUC(growing_repo=growing_repo)


#  self.growing_report = growing_report
#         self.common_repository = common_repository
#         self.query_helper = query_helper


def get_update_status_growing_report_uc(
    growing_repo: GrowingRepositoryDep,
    common_repo: CommonRepositoryDep,
    queyr_helper: QueryHelperDep,
) -> IUpdateStatusGrowingReportUC:
    return UpdateStatusGrowingReportUC(
        growing_repo=growing_repo, common_repo=common_repo, query_helper=queyr_helper
    )


CreateGrowingReportUseCaseDep = Annotated[
    ICreateGrowingReportUC, Depends(get_create_growing_report_uc)
]
GetListGrowingReportUseCaseDep = Annotated[
    IListGrowingReportUC, Depends(get_list_growing_report_uc)
]
UpdateStatusGrowingReportUseCaseDep = Annotated[
    IUpdateStatusGrowingReportUC, Depends(get_update_status_growing_report_uc)
]
