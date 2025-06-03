from typing import Annotated

from fastapi import Depends

from app.application.interfaces.use_cases.zone.create_zone_uc import ICreateZoneUC
from app.application.interfaces.use_cases.zone.list_zone_uc import IListZoneUC
from app.application.interfaces.use_cases.zone.update_status_zone_level_uc import (
    IUpdateStatusZoneLevelUC,
)
from app.application.interfaces.use_cases.zone.update_status_zone_uc import (
    IUpdateStatusZoneUC,
)
from app.application.interfaces.use_cases.zone.update_zone_uc import IUpdateZoneUC
from app.application.use_cases.zone.create_zone_uc_impl import CreateZoneUC
from app.application.use_cases.zone.list_zone_uc_impl import ListZoneUC
from app.application.use_cases.zone.update_status_zone_level_uc_impl import (
    UpdateStatusZoneLevelUC,
)
from app.application.use_cases.zone.update_status_zone_uc_impl import UpdateStatusZoneUC
from app.application.use_cases.zone.update_zone_uc_impl import UpdateZoneUC
from app.domain.interfaces.repositories.zone_repository import IZoneRepository
from app.infrastructure.database.repositories.zone_repository_impl import ZoneRepository
from app.presentation.api.v1.dependencies.common_dependencies import (
    DatabaseDep,
    QueryHelperDep,
)


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


def get_update_status_zone_level_uc(
    zone_repo: ZoneRepositoryDep,
) -> IUpdateStatusZoneLevelUC:
    return UpdateStatusZoneLevelUC(repo=zone_repo)


GetListZoneUseCaseDep = Annotated[IListZoneUC, Depends(get_list_zone_uc)]
CreateZoneUseCaseDep = Annotated[ICreateZoneUC, Depends(get_create_zone_uc)]
UpdateZoneUseCaseDep = Annotated[IUpdateZoneUC, Depends(get_update_zone_uc)]
UpdateStatusZoneUseCaseDep = Annotated[
    IUpdateStatusZoneUC, Depends(get_update_status_zone_uc)
]
UpdateStatusZoneLevelUseCaseDep = Annotated[
    IUpdateStatusZoneLevelUC, Depends(get_update_status_zone_level_uc)
]
