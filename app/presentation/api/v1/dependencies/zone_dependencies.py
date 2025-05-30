from typing import Annotated

from fastapi import Depends

from application.interfaces.use_cases.zone.create_zone_uc import ICreateZoneUC
from application.interfaces.use_cases.zone.list_zone_uc import IListZoneUC
from application.interfaces.use_cases.zone.update_status_zone_uc import \
    IUpdateStatusZoneUC
from application.interfaces.use_cases.zone.update_zone_uc import IUpdateZoneUC
from application.use_cases.zone.create_zone_uc_impl import CreateZoneUC
from application.use_cases.zone.list_zone_uc_impl import ListZoneUC
from application.use_cases.zone.update_status_zone_uc_impl import \
    UpdateStatusZoneUC
from application.use_cases.zone.update_zone_uc_impl import UpdateZoneUC
from domain.interfaces.repositories.zone_repository import IZoneRepository
from infrastructure.database.repositories.zone_repository_impl import \
    ZoneRepository
from presentation.api.v1.dependencies.common_dependencies import (
    DatabaseDep, QueryHelperDep)


def get_zone_repository(
    db: DatabaseDep, query_helper: QueryHelperDep
) -> IZoneRepository:
    return ZoneRepository(conn=db, query_helper=query_helper)


ZoneRepositoryDep = Annotated[IZoneRepository, Depends(get_zone_repository)]


def get_list_zone_uc(
    zone_repo: ZoneRepositoryDep,
) -> IListZoneUC:
    return ListZoneUC(zone_repo=zone_repo)


def get_create_zone_uc(
    zone_repo: ZoneRepositoryDep,
) -> ICreateZoneUC:
    return CreateZoneUC(zone_repo=zone_repo)


def get_update_zone_uc(
    zone_repo: ZoneRepositoryDep,
) -> IUpdateZoneUC:
    return UpdateZoneUC(zone_repo=zone_repo)


def get_update_status_zone_uc(
    zone_repo: ZoneRepositoryDep,
) -> IUpdateStatusZoneUC:
    return UpdateStatusZoneUC(zone_repo=zone_repo)


GetListZoneUseCaseDep = Annotated[IListZoneUC, Depends(get_list_zone_uc)]
CreateZoneUseCaseDep = Annotated[ICreateZoneUC, Depends(get_create_zone_uc)]
UpdateZoneUseCaseDep = Annotated[IUpdateZoneUC, Depends(get_update_zone_uc)]
UpdateStatusZoneUseCaseDep = Annotated[
    IUpdateStatusZoneUC, Depends(get_update_status_zone_uc)
]
