from app.application.dto.operation_type_dto import OperationTypeDTO
from app.application.interfaces.use_cases.operation_type.update_status_operation_type_uc import (
    IUpdateStatusOperationTypeUC,
)
from app.core.exception import BadRequestError
from app.domain.entities.operation_type_entity import OperationTypeEntity
from app.domain.interfaces.repositories.operation_type_repository import (
    IOperationTypeRepository,
)


class UpdateStatusOperationTypeUC(IUpdateStatusOperationTypeUC):
    def __init__(self, repo: IOperationTypeRepository):
        self.repo = repo

    def execute(self, operation_type_dto: OperationTypeDTO) -> bool:
        query_entity = OperationTypeEntity(id=operation_type_dto.id)

        operation_type_entity = self.repo.get_operation_type_by_id(
            operation_type_entity=query_entity
        )

        if operation_type_entity is None:
            raise BadRequestError("ETB-loai_san_pham_khong_ton_tai")

        if operation_type_entity.is_active == query_entity.is_active:
            return True

        operation_type_entity.change_is_active(
            is_active=operation_type_dto.is_active)

        is_success = self.repo.update_status_operation_type(
            operation_type_entity=operation_type_entity
        )

        if not is_success:
            raise BadRequestError(
                "ETB-cap_nhat_trang_thai_loai_san_pham_that_bai")

        return True
