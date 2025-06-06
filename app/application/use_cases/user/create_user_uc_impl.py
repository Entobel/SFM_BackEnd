from app.application.interfaces.use_cases.user.create_user_uc import ICreateUserUC
from app.core.exception import BadRequestError
from app.domain.entities.department_entity import DepartmentEntity
from app.domain.entities.department_factory_entity import DepartmentFactoryEntity
from app.domain.entities.department_factory_role_entity import \
    DepartmentFactoryRoleEntity
from app.domain.entities.factory_entity import FactoryEntity
from app.domain.entities.role_entity import RoleEntity
from app.domain.entities.user_entity import UserEntity
from app.domain.interfaces.repositories.user_repository import IUserRepository
from app.domain.interfaces.services.password_service import IPasswordService
from app.presentation.schemas.user_schema import CreateUserInputSchema


class CreateUserUC(ICreateUserUC):
    def __init__(
        self, user_repository: IUserRepository, password_service: IPasswordService
    ):
        self.user_repository = user_repository
        self.password_service = password_service

    def execute(self, user_dto: CreateUserInputSchema) -> UserEntity:
        is_exist_email_or_phone = self.user_repository.get_user_by_email_and_phone(
            email=user_dto.email, phone=user_dto.phone
        )

        if is_exist_email_or_phone["is_exist_email"] != 0:
            raise BadRequestError(
                details=[{"field": "email", "code": "ETB-email_da_ton_tai"}]
            )

        if is_exist_email_or_phone["is_exist_phone"] != 0:
            raise BadRequestError(
                details=[{"field": "phone", "code": "ETB-phone_da_ton_tai"}]
            )

        hashed_password = self.password_service.hash_password(user_dto.password)

        user = UserEntity(
            email=user_dto.email,
            phone=user_dto.phone,
            first_name=user_dto.first_name,
            last_name=user_dto.last_name,
            password=hashed_password,
            department_factory_role=DepartmentFactoryRoleEntity(
                department_factory=DepartmentFactoryEntity(
                    department=DepartmentEntity(id=user_dto.department_id),
                    factory=FactoryEntity(id=user_dto.factory_id),
                ),
                role=RoleEntity(id=user_dto.role_id),
            ),
        )

        is_success = self.user_repository.create_user(user)

        if not is_success:
            raise BadRequestError("ETB-tao_tai_khoan_that_bai")

        return user
