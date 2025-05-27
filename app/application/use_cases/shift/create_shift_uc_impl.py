from application.interfaces.use_cases.shift.create_shift_uc import \
    ICreateShiftUC
from application.schemas.shift_schemas import ShiftDTO
from core.exception import BadRequestError
from domain.entities.shift_entity import ShiftEntity
from domain.interfaces.repositories.shift_repository import IShiftRepository


class CreateShiftUC(ICreateShiftUC):
    def __init__(self, shift_repository: IShiftRepository):
        self.shift_repository = shift_repository

    def execute(self, shift_dto: ShiftDTO) -> bool:
        if self.shift_repository.get_shift_by_name(shift_dto.name):
            raise BadRequestError("ETB-shift_da_ton_tai")

        shift_entity = ShiftEntity(
            name=shift_dto.name,
            description=shift_dto.description,
        )

        is_success = self.shift_repository.create_shift(shift_entity)

        if not is_success:
            raise BadRequestError("ETB-tao_shift_that_bai")

        return True
