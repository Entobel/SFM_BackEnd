from app.application.dto.operation_type_dto import OperationTypeDTO
from app.application.interfaces.use_cases.operation_type.create_operation_type_uc import \
    ICreateOperationTypeUC
from app.core.exception import BadRequestError
from app.domain.entities.operation_type_entity import OperationTypeEntity
from app.domain.interfaces.repositories.operation_type_repository import \
    IOperationTypeRepository


class CreateOperationTypeUC(ICreateOperationTypeUC):
    def __init__(self, repo: IOperationTypeRepository):
        self.repo = repo

    def execute(self, operation_type_dto: OperationTypeDTO) -> bool:

        if self.repo.get_operation_type_by_name(operation_type_dto.name):
            raise BadRequestError("ETB-loai_san_pham_da_ton_tai")

        production_entity = OperationTypeEntity(
            name=operation_type_dto.name,
            abbr_name=operation_type_dto.abbr_name,
            description=operation_type_dto.description,
        )

        is_success = self.repo.create_operation_type(production_entity)

        if not is_success:
            raise BadRequestError("ETB-tao_loai_san_pham_that_bai")

        return True
