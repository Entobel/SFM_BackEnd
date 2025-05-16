from core.exception import BadRequestError
from application.schemas.role_schemas import RoleDTO
from domain.entities.role_entity import RoleEntity
from domain.interfaces.repositories.role_repository import IRoleRepository
from application.interfaces.use_cases.role.create_role_uc import ICreateRoleUC


class CreateRoleUC(ICreateRoleUC):
    def __init__(self, role_repository: IRoleRepository):
        self.role_repository = role_repository

    def execute(self, role: RoleDTO) -> bool:
        role_by_name = self.role_repository.get_role_by_name(role.name)

        if role_by_name:
            raise BadRequestError("ETB-ten_vai_tro_da_ton_tai")

        role_entity = RoleEntity(
            name=role.name,
            description=role.description,
        )

        result = self.role_repository.create_role(role=role_entity)

        if result:
            return role_entity
        else:
            raise BadRequestError("ETB-tao_vai_tro_that_bai")
