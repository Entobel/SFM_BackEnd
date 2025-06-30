from typing import Annotated

from fastapi import Depends
from app.application.interfaces.use_cases.harvesting.create_harvesting_report_uc import (
    ICreateHarvestingReportUC,
)
from app.application.interfaces.use_cases.harvesting.delete_harvesting_report_uc import (
    IDeleteHarvestingReportUC,
)
from app.application.interfaces.use_cases.harvesting.list_harvesting_report_uc import (
    IListHarvestingReportUC,
)
from app.application.interfaces.use_cases.harvesting.update_harvesting_report_uc import (
    IUpdateHarvestingReportUC,
)
from app.application.use_cases.harvesting.create_harvesting_report_uc_impl import (
    CreateHarvestingReportUC,
)
from app.application.use_cases.harvesting.delete_harvesting_report_uc_impl import (
    DeleteHarvestingReportUC,
)
from app.application.use_cases.harvesting.list_harvesting_report_uc_impl import (
    ListHarvestingReportUC,
)
from app.application.use_cases.harvesting.update_harvesting_report_uc_impl import (
    UpdateHarvestingReport,
)
from app.domain.interfaces.repositories.harvesting_repository import (
    IHarvestingRepository,
)
from app.infrastructure.database.repositories.harvesting_repository_impl import (
    HarvestingRepository,
)
from app.presentation.api.v1.dependencies.common_dependencies import (
    CommonRepositoryDep,
    DatabaseDep,
    QueryHelperDep,
)
from app.presentation.api.v1.dependencies.zone_dependencies import ZoneRepositoryDep


def get_harvest_repository(
    db: DatabaseDep, query_helper: QueryHelperDep
) -> IHarvestingRepository:
    return HarvestingRepository(conn=db, query_helper=query_helper)


HarvestingRepositoryDep = Annotated[
    IHarvestingRepository, Depends(get_harvest_repository)
]


def get_create_harvesting_report_uc(
    harvesting_repo: HarvestingRepositoryDep,
    zone_repo: ZoneRepositoryDep,
    common_repo: CommonRepositoryDep,
    query_helper: QueryHelperDep,
) -> ICreateHarvestingReportUC:
    return CreateHarvestingReportUC(
        harvesting_repo=harvesting_repo,
        zone_repo=zone_repo,
        query_helper=query_helper,
        common_repo=common_repo,
    )


def get_list_harvesting_report_uc(
    harvesting_repo: HarvestingRepositoryDep,
) -> IListHarvestingReportUC:
    return ListHarvestingReportUC(harvesting_repo=harvesting_repo)


def get_update_harvesting_report_uc(
    harvesting_repo: HarvestingRepositoryDep,
    common_repo: CommonRepositoryDep,
    query_helper: QueryHelperDep,
) -> IUpdateHarvestingReportUC:
    return UpdateHarvestingReport(
        harvesting_repo=harvesting_repo,
        common_repo=common_repo,
        query_helper=query_helper,
    )


def get_delete_harvesting_report_uc(
    harvesting_repo: HarvestingRepositoryDep,
) -> IDeleteHarvestingReportUC:
    return DeleteHarvestingReportUC(harvesting_repo=harvesting_repo)


CreateHarvestingReportUseCaseDep = Annotated[
    ICreateHarvestingReportUC, Depends(get_create_harvesting_report_uc)
]

GetListHarvestingReportUseCaseDep = Annotated[
    IListHarvestingReportUC, Depends(get_list_harvesting_report_uc)
]

UpdateHarvestingReportUseCaseDep = Annotated[
    IUpdateHarvestingReportUC, Depends(get_update_harvesting_report_uc)
]

DeleteHarvestingReportUseCaseDep = Annotated[
    IDeleteHarvestingReportUC, Depends(get_delete_harvesting_report_uc)
]
