from core.exception import BadRequestError
from application.schemas.department_schemas import DepartmentDTO
from application.interfaces.use_cases.department.update_department_uc import (
    IUpdateDepartmentUC,
)
from domain.interfaces.repositories.department_repository import IDepartmentRepository


class UpdateDepartmentUC(IUpdateDepartmentUC):
    def __init__(self, department_repository: IDepartmentRepository):
        self.department_repository = department_repository

    def execute(self, department_id: int, department_dto: DepartmentDTO) -> bool:
        department = self.department_repository.get_department_by_id(department_id)
        print("department", department_dto)
        if not department:
            raise BadRequestError(error_code="ETB-phong_ban_khong_ton_tai")

        if department_dto.name != department.name:
            is_exist_name = self.department_repository.get_department_by_name(
                department_dto.name
            )

            if is_exist_name:
                raise BadRequestError(error_code="ETB-phong_ban_da_ton_tai")

        if department_dto.parent_id:
            department.set_parent_id(department_dto.parent_id)

        if department_dto.name:
            department.set_name(department_dto.name)

        if department_dto.abbr_name:
            department.set_abbr_name(department_dto.abbr_name)

        if department_dto.description:
            department.set_description(department_dto.description)

        is_updated = self.department_repository.update_department(department)

        if not is_updated:
            raise BadRequestError(error_code="ETB-cap_nhat_phong_ban_that_bai")

        return True
