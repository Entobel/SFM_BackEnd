from app.application.dto.role_dto import RoleDTO
from app.application.interfaces.use_cases.role.create_role_uc import ICreateRoleUC
from app.core.exception import BadRequestError
from app.domain.entities.role_entity import RoleEntity
from app.domain.interfaces.repositories.role_repository import IRoleRepository


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
