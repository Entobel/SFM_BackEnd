from typing import Annotated

from fastapi import Depends
from application.use_cases.shift.list_shift_uc_impl import ListShiftUC
from application.interfaces.use_cases.shift.list_shift_uc import IListShiftUC
from infrastructure.database.repositories.shift_repository_impl import (
    ShiftRepository,
)
from presentation.api.v1.dependencies.common_dependencies import DatabaseDep
from domain.interfaces.repositories.shift_repository import IShiftRepository


def get_shift_repository(db: DatabaseDep) -> IShiftRepository:
    return ShiftRepository(conn=db)


def get_list_shift_use_case(
    shift_repository: Annotated[IShiftRepository, Depends(get_shift_repository)],
) -> IListShiftUC:
    return ListShiftUC(shift_repository=shift_repository)


ListShiftUCDep = Annotated[IListShiftUC, Depends(get_list_shift_use_case)]
