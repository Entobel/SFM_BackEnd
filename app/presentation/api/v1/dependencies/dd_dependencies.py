from typing import Annotated

from fastapi import Depends
from app.application.interfaces.use_cases.dd.create_dd_report_uc import (
    ICreateDdReportUC,
)
from app.application.interfaces.use_cases.dd.list_dd_report_uc import IListDdReportUC
from app.application.interfaces.use_cases.dd.update_dd_report_uc import (
    IUpdateDdReportUC,
)
from app.application.use_cases.dd.create_dd_report_uc_impl import CreateDDReportUC
from app.application.use_cases.dd.list_dd_report_uc_impl import ListDdReportUC
from app.application.use_cases.dd.update_dd_report_uc_impl import UpdateDdReportUC
from app.domain.interfaces.repositories.dd_repository import IDdRepository
from app.infrastructure.database.repositories.dd_repository_impl import DDRepository
from app.presentation.api.v1.dependencies.common_dependencies import (
    CommonRepositoryDep,
    DatabaseDep,
    QueryHelperDep,
)


def get_dd_repository(conn: DatabaseDep, query_helper: QueryHelperDep) -> IDdRepository:
    return DDRepository(conn=conn, query_helper=query_helper)


GetDDRepositoryDep = Annotated[IDdRepository, Depends(get_dd_repository)]


def get_create_dd_report_uc(
    dd_repository: GetDDRepositoryDep,
    query_helper: QueryHelperDep,
    common_repository: CommonRepositoryDep,
) -> ICreateDdReportUC:
    return CreateDDReportUC(
        dd_repository=dd_repository,
        common_repository=common_repository,
        query_helper=query_helper,
    )


def get_list_dd_report_uc(dd_repository: GetDDRepositoryDep) -> IListDdReportUC:
    return ListDdReportUC(dd_repo=dd_repository)


def get_update_dd_report_uc(
    dd_repository: GetDDRepositoryDep,
    query_helper: QueryHelperDep,
    common_repository: CommonRepositoryDep,
) -> IUpdateDdReportUC:
    return UpdateDdReportUC(
        dd_repository=dd_repository,
        common_repository=common_repository,
        query_helper=query_helper,
    )


CreateDdReportUseCaseDep = Annotated[
    ICreateDdReportUC, Depends(get_create_dd_report_uc)
]

ListDdReportUseCaseDep = Annotated[IListDdReportUC, Depends(get_list_dd_report_uc)]

UpdateDdReportUseCaseDep = Annotated[
    IUpdateDdReportUC, Depends(get_update_dd_report_uc)
]
