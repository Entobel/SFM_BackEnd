from application.interfaces.use_cases.department.update_status_department_factory_role_uc import (
    IUpdateStatusDepartmentFactoryRoleUC,
)
from application.schemas.department_factory_role_schemas import DepartmentFactoryRoleDTO
from core.exception import BadRequestError, NotFoundError
from domain.interfaces.repositories.deparment_factory_role_repository import (
    IDepartmentFactoryRoleRepository,
)


class UpdateStatusDepartmentFactoryRoleUC(IUpdateStatusDepartmentFactoryRoleUC):
    def __init__(
        self, department_factory_role_repository: IDepartmentFactoryRoleRepository
    ):
        self.department_factory_role_repository = department_factory_role_repository

    def execute(self, department_factory_role_dto: DepartmentFactoryRoleDTO) -> bool:
        department_factory_role_entity = (
            self.department_factory_role_repository.get_department_factory_role_by_id(
                id=department_factory_role_dto.id
            )
        )

        if department_factory_role_entity is None:
            raise NotFoundError("ETB_khong_tim_thay_phong_ban_nha_may")

        if (
            department_factory_role_entity.is_active
            == department_factory_role_dto.is_active
        ):
            return True

        if not department_factory_role_dto.is_active:

            is_in_use = self.department_factory_role_repository.is_department_factory_role_in_use(
                department_factory_role_entity=department_factory_role_entity
            )

            if is_in_use:
                raise BadRequestError(
                    "ETB-phong_ban_nha_may_dang_duoc_su_dung_khong_the_deactivate"
                )

        department_factory_role_entity.change_status(
            department_factory_role_dto.is_active
        )

        is_success = self.department_factory_role_repository.update_status_department_factory_role(
            department_factory_role_entity=department_factory_role_entity
        )

        if not is_success:
            raise BadRequestError("ETB_cap_nhat_trang_thai_phong_ban_nha_may_that_bai")

        return True
