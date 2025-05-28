from application.interfaces.use_cases.department.create_department_factory_role_uc import (
    ICreateDepartmentFactoryRoleUC,
)
from application.schemas.department_factory_role_schemas import DepartmentFactoryRoleDTO
from core.exception import BadRequestError, NotFoundError
from domain.entities.department_factory_entity import DepartmentFactoryEntity
from domain.entities.department_factory_role_entity import DepartmentFactoryRoleEntity
from domain.entities.role_entity import RoleEntity
from domain.interfaces.repositories.deparment_factory_role_repository import (
    IDepartmentFactoryRoleRepository,
)
from domain.interfaces.repositories.role_repository import IRoleRepository


class CreateDepartmentFactoryRoleUC(ICreateDepartmentFactoryRoleUC):
    def __init__(
        self,
        role_repository: IRoleRepository,
        department_factory_role_repository: IDepartmentFactoryRoleRepository,
    ):
        self.role_repository = role_repository
        self.department_factory_role_repository = department_factory_role_repository

    def execute(self, department_factory_role_dto: DepartmentFactoryRoleDTO) -> bool:
        role_id = department_factory_role_dto.role.id

        # Check exist role by id
        role_entity = self.role_repository.get_role_by_id(id=role_id)

        if role_entity is None:
            raise NotFoundError("ETB-role_khong_ton_tai")

        department_factory_id = department_factory_role_dto.department_factory.id
        role_id = department_factory_role_dto.role.id

        print("Department factory id", department_factory_id, "Role", role_id)

        # Check if exist department factory
        is_exist = self.department_factory_role_repository.check_department_factory_role_exists(
            department_factory_role_entity=DepartmentFactoryRoleEntity(
                department_factory=DepartmentFactoryEntity(
                    id=department_factory_id,
                ),
                role=RoleEntity(
                    id=role_id,
                ),
            )
        )

        if is_exist:
            raise BadRequestError("ETB-department_factory_role_da_ton_tai")

        # Create department factory role
        department_factory_role_entity = DepartmentFactoryRoleEntity(
            department_factory=DepartmentFactoryEntity(
                id=department_factory_id,
            ),
            role=RoleEntity(
                id=role_id,
            ),
        )

        is_created = (
            self.department_factory_role_repository.create_department_factory_role(
                department_factory_role_entity=department_factory_role_entity
            )
        )

        if not is_created:
            raise BadRequestError("ETB-tao_phong_ban_cua_nha_may_vai_tro_that_bai")

        return True
