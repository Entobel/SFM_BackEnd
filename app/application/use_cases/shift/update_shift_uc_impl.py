from application.interfaces.use_cases.shift.update_shift_uc import IUpdateShiftUC
from application.schemas.shift_dto import ShiftDTO
from core.exception import BadRequestError
from domain.interfaces.repositories.shift_repository import IShiftRepository


class UpdateShiftUC(IUpdateShiftUC):
    def __init__(self, shift_repository: IShiftRepository):
        self.shift_repository = shift_repository

    def execute(self, shift_dto: ShiftDTO) -> bool:
        shift_entity = self.shift_repository.get_shift_by_id(shift_dto.id)
        if not shift_entity:
            raise BadRequestError("ETB-shift_khong_ton_tai")

        if shift_dto.name is not None and shift_dto.name != shift_entity.name:

            if self.shift_repository.get_shift_by_name(shift_dto.name):
                raise BadRequestError("ETB-ten_ca_lam_da_ton_tai")

            shift_entity.change_name(shift_dto.name)

        if (
            shift_dto.description is not None
            and shift_dto.description != shift_entity.description
        ):
            shift_entity.change_description(shift_dto.description)

        is_success = self.shift_repository.update_shift(shift_entity=shift_entity)

        if not is_success:
            raise BadRequestError("ETB-cap_nhat_shift_that_bai")

        return True
