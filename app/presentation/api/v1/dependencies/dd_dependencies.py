from typing import Annotated

from fastapi import Depends
from app.application.interfaces.use_cases.dd.create_dd_report_uc import ICreateDdReportUC
from app.application.use_cases.dd.create_dd_report_uc_impl import CreateDDReportUC
from app.domain.interfaces.repositories.dd_repository import IDdRepository
from app.infrastructure.database.repositories.dd_repository_impl import DDRepository
from app.presentation.api.v1.dependencies.common_dependencies import CommonRepositoryDep, DatabaseDep, QueryHelperDep


def get_dd_repository(conn: DatabaseDep, query_helper: QueryHelperDep) -> IDdRepository:
    return DDRepository(conn=conn, query_helper=query_helper)


GetDDRepositoryDep = Annotated[IDdRepository, Depends(get_dd_repository)]


def get_create_dd_report_uc(dd_repository: GetDDRepositoryDep, query_helper: QueryHelperDep, common_repository: CommonRepositoryDep) -> ICreateDdReportUC:
    return CreateDDReportUC(dd_repository=dd_repository, common_repository=common_repository, query_helper=query_helper)


CreateDDReportUseCase = Annotated[ICreateDdReportUC, Depends(
    get_create_dd_report_uc)]
