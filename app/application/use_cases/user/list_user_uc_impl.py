from application.interfaces.use_cases.user.list_user_uc import IListUserUC
from domain.entities.user_entity import UserEntity
from domain.interfaces.repositories.user_repository import IUserRepository


class ListUserUC(IListUserUC):
    def __init__(self, user_repository: IUserRepository) -> None:
        self.user_repository = user_repository

    def execute(
        self,
        page: int,
        page_size: int,
        search: str,
        department_id: int,
        factory_id: int,
        role_id: int,
        is_active: bool,
    ) -> dict[
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
        "items" : list[UserEntity],
    ]:
        return self.user_repository.get_list_users(
            page, page_size, search, department_id, factory_id, role_id, is_active
        )
