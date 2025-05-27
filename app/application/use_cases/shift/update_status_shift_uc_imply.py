from application.interfaces.use_cases.shift.update_status_shift_uc import \
    IUpdateStatusShiftUC
from application.schemas.shift_schemas import ShiftDTO
from core.exception import BadRequestError
from domain.interfaces.repositories.shift_repository import IShiftRepository


class UpdateStatusShiftUC(IUpdateStatusShiftUC):
    def __init__(self, shift_repository: IShiftRepository):
        self.shift_repository = shift_repository

    def execute(self, shift_dto: ShiftDTO) -> bool:
        shift_entity = self.shift_repository.get_shift_by_id(shift_dto.id)
        if not shift_entity:
            raise BadRequestError("ETB-shift_khong_ton_tai")

        shift_entity.change_status(shift_dto.is_active)

        is_success = self.shift_repository.update_status_shift(
            shift_entity=shift_entity
        )

        if not is_success:
            raise BadRequestError("ETB-cap_nhat_trang_thai_shift_that_bai")

        return True
