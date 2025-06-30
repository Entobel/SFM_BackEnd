from typing import Annotated

from fastapi import Depends
from app.application.interfaces.use_cases.grinding.create_grinding_report_uc import (
    ICreateGrindingUC,
)
from app.application.interfaces.use_cases.grinding.delete_grinding_report_uc import (
    IDeleteGrindingReportUC,
)
from app.application.interfaces.use_cases.grinding.list_grinding_report_uc import (
    IListGrindingReportUC,
)
from app.application.interfaces.use_cases.grinding.update_grinding_report_uc import (
    IUpdateGrindingReportUC,
)
from app.application.use_cases.grinding.create_grinding_report_uc_impl import (
    CreateGrindingUC,
)
from app.application.use_cases.grinding.delete_grinding_report_uc_impl import (
    DeleteGrindingReportUC,
)
from app.application.use_cases.grinding.list_grinding_report_uc_impl import (
    ListGrindingReportUC,
)
from app.application.use_cases.grinding.update_grinding_report_uc_impl import (
    UpdateGrindingReportUC,
)
from app.domain.interfaces.repositories.grinding_repository import IGrindingRepository
from app.infrastructure.database.repositories.grinding_repository_impl import (
    GrindingRepository,
)
from app.presentation.api.v1.dependencies.common_dependencies import (
    CommonRepositoryDep,
    DatabaseDep,
    QueryHelperDep,
)


def get_grinding_repository(
    db: DatabaseDep, query_helper: QueryHelperDep
) -> IGrindingRepository:
    return GrindingRepository(conn=db, query_helper=query_helper)


GrindingRepositoryDep = Annotated[IGrindingRepository, Depends(get_grinding_repository)]


def get_create_grinding_uc(
    grinding_repo: GrindingRepositoryDep,
    common_repo: CommonRepositoryDep,
    query_helper: QueryHelperDep,
) -> ICreateGrindingUC:
    return CreateGrindingUC(
        grinding_repo=grinding_repo, common_repo=common_repo, query_helper=query_helper
    )


def get_list_grinding_report_uc(
    grinding_repo: GrindingRepositoryDep,
) -> IListGrindingReportUC:
    return ListGrindingReportUC(grinding_repo=grinding_repo)


def get_update_grinding_uc(
    grinding_repo: GrindingRepositoryDep,
    common_repo: CommonRepositoryDep,
    query_helper: QueryHelperDep,
) -> IUpdateGrindingReportUC:
    return UpdateGrindingReportUC(
        grinding_repo=grinding_repo, common_repo=common_repo, query_helper=query_helper
    )


def get_delete_grinding_report_uc(
    grinding_repo: GrindingRepositoryDep,
) -> IDeleteGrindingReportUC:
    return DeleteGrindingReportUC(grinding_repo=grinding_repo)


CreateGrindingUseCaseDep = Annotated[ICreateGrindingUC, Depends(get_create_grinding_uc)]

ListGrindingReportUseCaseDep = Annotated[
    IListGrindingReportUC, Depends(get_list_grinding_report_uc)
]
UpdateGrindingReportUseCaseDep = Annotated[
    IUpdateGrindingReportUC, Depends(get_update_grinding_uc)
]

DeleteGrindingReportUseCaseDep = Annotated[
    IDeleteGrindingReportUC, Depends(get_delete_grinding_report_uc)
]
