from fastapi import Depends
from typing import Annotated

from app.application.interfaces.use_cases.growing.create_growing_report_uc import (
    ICreateGrowingReportUC,
)
from app.application.use_cases.growing.create_growing_report_uc_impl import (
    CreateGrowingReportUC,
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


CreateGrowingReportUCDep = Annotated[
    ICreateGrowingReportUC, Depends(get_create_growing_report_uc)
]
