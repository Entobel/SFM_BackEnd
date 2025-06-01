from app.application.dto.department_dto import DepartmentDTO
from app.application.interfaces.use_cases.department.create_department_uc import \
    ICreateDepartmentUC
from app.core.exception import BadRequestError
from app.domain.entities.department_entity import DepartmentEntity
from app.domain.interfaces.repositories.department_repository import \
    IDepartmentRepository


class CreateDepartmentUC(ICreateDepartmentUC):
    def __init__(self, department_repository: IDepartmentRepository):
        self.department_repository = department_repository

    def execute(self, department: DepartmentDTO) -> bool:
        is_exist_name = self.department_repository.get_department_by_name(
            department.name
        )

        if is_exist_name:
            raise BadRequestError(
                error_code="ETB-phong_ban_da_ton_tai",
            )

        department = DepartmentEntity(
            name=department.name,
            abbr_name=department.abbr_name,
            description=department.description,
            parent_id=department.parent_id,
        )

        is_created = self.department_repository.create_department(department)

        if not is_created:
            raise BadRequestError(
                error_code="ETB-tao_phong_ban_that_bai",
            )

        return True
