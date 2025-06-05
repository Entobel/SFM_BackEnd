from typing import Annotated

from fastapi import Depends

from app.application.interfaces.use_cases.shift.create_shift_uc import ICreateShiftUC
from app.application.interfaces.use_cases.shift.list_shift_uc import IListShiftUC
from app.application.interfaces.use_cases.shift.update_shift_uc import IUpdateShiftUC
from app.application.interfaces.use_cases.shift.update_status_shift_uc import (
    IUpdateStatusShiftUC,
)
from app.application.use_cases.shift.create_shift_uc_impl import CreateShiftUC
from app.application.use_cases.shift.list_shift_uc_impl import ListShiftUC
from app.application.use_cases.shift.update_shift_uc_impl import UpdateShiftUC
from app.application.use_cases.shift.update_status_shift_uc_imply import (
    UpdateStatusShiftUC,
)
from app.domain.interfaces.repositories.shift_repository import IShiftRepository
from app.infrastructure.database.repositories.shift_repository_impl import (
    ShiftRepository,
)
from app.presentation.api.v1.dependencies.common_dependencies import (
    DatabaseDep,
    QueryHelperDep,
)


def get_shift_repository(
    db: DatabaseDep, query_helper: QueryHelperDep
) -> IShiftRepository:
    return ShiftRepository(conn=db, query_helper=query_helper)


ShiftRepositoryDep = Annotated[IShiftRepository, Depends(get_shift_repository)]


def get_list_shift_use_case(
    shift_repository: ShiftRepositoryDep,
) -> IListShiftUC:
    return ListShiftUC(shift_repository=shift_repository)


def get_create_shift_use_case(
    shift_repository: ShiftRepositoryDep,
) -> ICreateShiftUC:
    return CreateShiftUC(shift_repository=shift_repository)


def get_update_status_shift_use_case(
    shift_repository: ShiftRepositoryDep,
) -> IUpdateStatusShiftUC:
    return UpdateStatusShiftUC(shift_repository=shift_repository)


def get_update_shift_use_case(
    shift_repository: ShiftRepositoryDep,
) -> IUpdateShiftUC:
    return UpdateShiftUC(shift_repository=shift_repository)


ListShiftUCDep = Annotated[IListShiftUC, Depends(get_list_shift_use_case)]
CreateShiftUCDep = Annotated[ICreateShiftUC, Depends(get_create_shift_use_case)]
UpdateStatusShiftUCDep = Annotated[
    IUpdateStatusShiftUC, Depends(get_update_status_shift_use_case)
]
UpdateShiftUCDep = Annotated[IUpdateShiftUC, Depends(get_update_shift_use_case)]
