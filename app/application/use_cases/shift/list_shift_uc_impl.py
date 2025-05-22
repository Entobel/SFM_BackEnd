from application.schemas.shift_schemas import ShiftDTO
from domain.entities.shift_entity import ShiftEntity
from application.interfaces.use_cases.shift.list_shift_uc import IListShiftUC
from domain.interfaces.repositories.shift_repository import IShiftRepository


class ListShiftUC(IListShiftUC):
    def __init__(self, shift_repository: IShiftRepository):
        self.shift_repository = shift_repository

    def execute(self) -> list[ShiftEntity]:
        shifts = self.shift_repository.get_all_shifts()

        return [ShiftDTO.model_validate(shift) for shift in shifts]
