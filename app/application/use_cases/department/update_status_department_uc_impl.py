from application.interfaces.use_cases.department.update_status_department_uc import \
    IUpdateStatusDepartmentUC
from core.exception import BadRequestError
from domain.interfaces.repositories.department_repository import \
    IDepartmentRepository


class UpdateStatusDepartmentUC(IUpdateStatusDepartmentUC):
    def __init__(self, department_repository: IDepartmentRepository):
        self.department_repository = department_repository

    def execute(self, department_id: int, is_active: bool) -> bool:
        department = self.department_repository.get_department_by_id(department_id)

        if not department:
            raise BadRequestError(error_code="ETB-phong_ban_khong_ton_tai")

        if department.is_active == is_active:
            return True

        if not is_active:
            is_in_use = self.department_repository.is_department_in_use(
                department=department
            )

            if is_in_use:
                raise BadRequestError(
                    error_code="ETB-phong_ban_dang_duoc_su_dung_khong_the_deactivate"
                )

        department.set_is_active(is_active)

        is_updated = self.department_repository.update_status_department(department)

        if not is_updated:
            raise BadRequestError(
                error_code="ETB-cap_nhat_trang_thai_phong_ban_that_bai"
            )

        return True
