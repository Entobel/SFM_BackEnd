from typing import Annotated

from fastapi import Depends
from app.application.interfaces.use_cases.vfbd.create_vfbd_report_uc import ICreateVfbdReportUC
from app.application.use_cases.vfbd.create_vfbd_report_uc_impl import CreateVfbdReportUC
from app.domain.interfaces.repositories.vfbd_repository import IVfbdRepository
from app.infrastructure.database.repositories.vfbd_repository_impl import VfbdRepository
from app.presentation.api.v1.dependencies.common_dependencies import CommonRepositoryDep, DatabaseDep, QueryHelperDep


def get_vfbd_repository(conn: DatabaseDep, query_helper: QueryHelperDep) -> IVfbdRepository:
    return VfbdRepository(conn=conn, query_helper=query_helper)


VfbdRepositoryDep = Annotated[IVfbdRepository, Depends(get_vfbd_repository)]


def get_create_vfbd_report_uc(vfbd_repository: VfbdRepositoryDep, common_repo: CommonRepositoryDep, query_helper: QueryHelperDep) -> ICreateVfbdReportUC:
    return CreateVfbdReportUC(vfbd_repository=vfbd_repository, common_repository=common_repo, query_helper=query_helper)


CreateVfbdReportUseCase = Annotated[ICreateVfbdReportUC, Depends(
    get_create_vfbd_report_uc)]
