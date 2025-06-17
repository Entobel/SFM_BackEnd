from app.application.dto.operation_type_dto import OperationTypeDTO
from app.application.interfaces.use_cases.operation_type.update_operation_type_uc import (
    IUpdateOperationTypeUC,
)
from app.core.exception import BadRequestError
from app.domain.entities.operation_type_entity import OperationTypeEntity
from app.domain.interfaces.repositories.operation_type_repository import (
    IOperationTypeRepository,
)


class UpdateOperationTypeUC(IUpdateOperationTypeUC):
    def __init__(self, repo: IOperationTypeRepository):
        self.repo = repo

    def execute(self, operation_type_dto: OperationTypeDTO) -> bool:
        query_entity = OperationTypeEntity(id=operation_type_dto.id)

        operation_type_entity = self.repo.get_operation_type_by_id(
            operation_type_entity=query_entity
        )

        if not operation_type_entity:
            raise BadRequestError("ETB-loai_san_pham_khong_ton_tai")

        if (
            query_entity.name is not None
            and query_entity.name != operation_type_entity.name
        ):
            if self.repo.get_operation_type_by_name(query_entity.name):
                raise BadRequestError("ETB-ten_loai_san_pham_da_ton_tai")

            operation_type_entity.change_name(query_entity.name)

        if (
            query_entity.abbr_name is not None
            and query_entity.abbr_name != operation_type_entity.abbr_name
        ):
            operation_type_entity.change_abbr_name(query_entity.abbr_name)

        if (
            query_entity.description is not None
            and query_entity.description != operation_type_entity.description
        ):
            operation_type_entity.change_description(query_entity.description)

        is_success = self.repo.update_operation_type(operation_type_entity)

        if not is_success:
            raise BadRequestError("ETB-cap_nhat_loai_san_pham_that_bai")

        return True
