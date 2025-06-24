from typing import Annotated

from fastapi import Depends
from app.application.interfaces.use_cases.vfbd.create_vfbd_report_uc import (
    ICreateVfbdReportUC,
)
from app.application.interfaces.use_cases.vfbd.list_vfbd_report_uc import (
    IListVfbdReportUC,
)
from app.application.interfaces.use_cases.vfbd.update_vfbd_report_uc import (
    IUpdateVfbdReportUC,
)
from app.application.use_cases.vfbd.create_vfbd_report_uc_impl import CreateVfbdReportUC
from app.application.use_cases.vfbd.list_vfbd_report_uc_impl import ListVfbdReportUC
from app.application.use_cases.vfbd.update_vfbd_report_uc_impl import UpdateVfbdReportUC
from app.domain.interfaces.repositories.vfbd_repository import IVfbdRepository
from app.infrastructure.database.repositories.vfbd_repository_impl import VfbdRepository
from app.presentation.api.v1.dependencies.common_dependencies import (
    CommonRepositoryDep,
    DatabaseDep,
    QueryHelperDep,
)


def get_vfbd_repository(
    conn: DatabaseDep, query_helper: QueryHelperDep
) -> IVfbdRepository:
    return VfbdRepository(conn=conn, query_helper=query_helper)


VfbdRepositoryDep = Annotated[IVfbdRepository, Depends(get_vfbd_repository)]


def get_create_vfbd_report_uc(
    vfbd_repository: VfbdRepositoryDep,
    common_repo: CommonRepositoryDep,
    query_helper: QueryHelperDep,
) -> ICreateVfbdReportUC:
    return CreateVfbdReportUC(
        vfbd_repository=vfbd_repository,
        common_repository=common_repo,
        query_helper=query_helper,
    )


def get_list_vfbd_report_uc(vfbd_repository: VfbdRepositoryDep) -> IListVfbdReportUC:
    return ListVfbdReportUC(vfbd_repo=vfbd_repository)


def get_update_vfbd_report_uc(
    vfbd_repository: VfbdRepositoryDep,
    common_repo: CommonRepositoryDep,
    query_helper: QueryHelperDep,
) -> IUpdateVfbdReportUC:
    return UpdateVfbdReportUC(
        vfbd_repository=vfbd_repository,
        common_repository=common_repo,
        query_helper=query_helper,
    )


CreateVfbdReportUseCaseDep = Annotated[
    ICreateVfbdReportUC, Depends(get_create_vfbd_report_uc)
]

ListVfbdReportUseCaseDep = Annotated[
    IListVfbdReportUC, Depends(get_list_vfbd_report_uc)
]

UpdateVfbdReportUseCaseDep = Annotated[
    IUpdateVfbdReportUC, Depends(get_update_vfbd_report_uc)
]
