from typing import Annotated

from fastapi import Depends
from application.interfaces.use_cases.shift.update_shift_uc import IUpdateShiftUC
from application.use_cases.shift.update_shift_uc_impl import UpdateShiftUC
from application.interfaces.use_cases.shift.update_status_shift_uc import (
    IUpdateStatusShiftUC,
)
from application.use_cases.shift.update_status_shift_uc_imply import UpdateStatusShiftUC
from application.use_cases.shift.create_shift_uc_impl import CreateShiftUC
from application.interfaces.use_cases.shift.create_shift_uc import ICreateShiftUC
from application.use_cases.shift.list_shift_uc_impl import ListShiftUC
from application.interfaces.use_cases.shift.list_shift_uc import IListShiftUC
from infrastructure.database.repositories.shift_repository_impl import (
    ShiftRepository,
)
from presentation.api.v1.dependencies.common_dependencies import (
    DatabaseDep,
    QueryHelperDep,
)
from domain.interfaces.repositories.shift_repository import IShiftRepository


def get_shift_repository(
    db: DatabaseDep, query_helper: QueryHelperDep
) -> IShiftRepository:
    return ShiftRepository(conn=db, query_helper=query_helper)


def get_list_shift_use_case(
    shift_repository: Annotated[IShiftRepository, Depends(get_shift_repository)],
) -> IListShiftUC:
    return ListShiftUC(shift_repository=shift_repository)


def get_create_shift_use_case(
    shift_repository: Annotated[IShiftRepository, Depends(get_shift_repository)],
) -> ICreateShiftUC:
    return CreateShiftUC(shift_repository=shift_repository)


def get_update_status_shift_use_case(
    shift_repository: Annotated[IShiftRepository, Depends(get_shift_repository)],
) -> IUpdateStatusShiftUC:
    return UpdateStatusShiftUC(shift_repository=shift_repository)


def get_update_shift_use_case(
    shift_repository: Annotated[IShiftRepository, Depends(get_shift_repository)],
) -> IUpdateShiftUC:
    return UpdateShiftUC(shift_repository=shift_repository)


ListShiftUCDep = Annotated[IListShiftUC, Depends(get_list_shift_use_case)]
CreateShiftUCDep = Annotated[ICreateShiftUC, Depends(get_create_shift_use_case)]
UpdateStatusShiftUCDep = Annotated[
    IUpdateStatusShiftUC, Depends(get_update_status_shift_use_case)
]
UpdateShiftUCDep = Annotated[IUpdateShiftUC, Depends(get_update_shift_use_case)]
