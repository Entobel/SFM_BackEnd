from application.interfaces.use_cases.department.update_status_department_factory_uc import \
    IUpdateStatusDepartmentFactoryUC
from application.schemas.department_factory_schemas import DepartmentFactoryDTO
from core.exception import BadRequestError, NotFoundError
from domain.interfaces.repositories.department_factory_repository import \
    IDepartmentFactoryRepository


class UpdateStatusDepartmentFactoryUC(IUpdateStatusDepartmentFactoryUC):
    def __init__(self, department_factory_repo: IDepartmentFactoryRepository):
        self.department_factory_repo = department_factory_repo

    def execute(self, department_factory_dto: DepartmentFactoryDTO) -> bool:
        department_factory_entity = (
            self.department_factory_repo.get_department_factory_by_id(
                id=department_factory_dto.id
            )
        )

        if not department_factory_entity:
            raise NotFoundError("ETB-phong_ban_nha_may_khong_ton_tai")

        if department_factory_entity.is_active == department_factory_dto.is_active:
            return True

        department_factory_entity.set_status(is_active=department_factory_dto.is_active)

        is_updated = self.department_factory_repo.update_status_department_factory(
            department_factory_entity=department_factory_entity
        )

        if not is_updated:
            raise BadRequestError("ETB-cap_nhat_trang_thai_phong_ban_nha_may_that_bai")

        return is_updated
