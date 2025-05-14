from abc import ABC, abstractmethod

from domain.entities.user_entity import UserEntity


class IListUserUC(ABC):
    @abstractmethod
    def execute(
        self,
        page: int,
        page_size: int,
        search: str,
        department_id: int,
        factory_id: int,
        role_id: int,
    ) -> dict[
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
        "items" : list[UserEntity],
    ]: ...
