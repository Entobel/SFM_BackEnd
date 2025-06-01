from app.application.dto.shift_dto import ShiftDTO
from app.application.interfaces.use_cases.shift.create_shift_uc import \
    ICreateShiftUC
from app.core.exception import BadRequestError
from app.domain.entities.shift_entity import ShiftEntity
from app.domain.interfaces.repositories.shift_repository import IShiftRepository


class CreateShiftUC(ICreateShiftUC):
    def __init__(self, shift_repository: IShiftRepository):
        self.shift_repository = shift_repository

    def execute(self, shift_dto: ShiftDTO) -> bool:
        shift_entity = ShiftEntity(
            name=shift_dto.name,
            description=shift_dto.description,
        )

        if self.shift_repository.get_shift_by_name(shift_entity=shift_entity):
            raise BadRequestError("ETB-shift_da_ton_tai")

        is_success = self.shift_repository.create_shift(shift_entity)

        if not is_success:
            raise BadRequestError("ETB-tao_shift_that_bai")

        return True
