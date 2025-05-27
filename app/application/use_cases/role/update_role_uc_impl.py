from application.interfaces.use_cases.role.update_role_uc import IUpdateRoleUC
from application.schemas.role_schemas import RoleDTO
from core.exception import BadRequestError
from domain.entities.role_entity import RoleEntity
from domain.interfaces.repositories.role_repository import IRoleRepository


class UpdateRoleUC(IUpdateRoleUC):
    def __init__(self, role_repository: IRoleRepository):
        self.role_repository = role_repository

    def execute(self, role_dto: RoleDTO) -> bool:
        role = self.role_repository.get_role_by_id(role_dto.id)
        if not role:
            raise BadRequestError("ETB-vai_tro_khong_ton_tai")

        if role_dto.name != role.name:
            existing_role = self.role_repository.get_role_by_name(role_dto.name)
            if existing_role:
                raise BadRequestError("ETB-ten_vai_tro_da_ton_tai")
            role.set_name(name=role_dto.name)

        if (
            role_dto.description is not None
            and role_dto.description != role.description
        ):
            role.set_description(description=role_dto.description)

        result = self.role_repository.update_role(
            RoleEntity(id=role.id, name=role.name, description=role.description)
        )

        if not result:
            raise BadRequestError("ETB-cap_nhat_vai_tro_that_bai")

        return True
