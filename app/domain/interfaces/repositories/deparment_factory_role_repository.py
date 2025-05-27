from abc import ABC, abstractmethod

from domain.entities.department_factory_role_entity import \
    DepartmentFactoryRoleEntity


class IDepartmentFactoryRoleRepository(ABC):
    @abstractmethod
    def check_department_factory_role_exists(
        self, department_id: int, factory_id: int, role_id: int
    ) -> bool: ...

    @abstractmethod
    def create_department_factory_role(
        self, department_id: int, factory_id: int, role_id: int
    ) -> int: ...

    @abstractmethod
    def get_list_department_factory_role(
        self,
        page: int,
        page_size: int,
        search: str,
        is_active: bool,
        department_id: int,
        factory_id: int,
    ) -> dict[
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
        "items" : list[DepartmentFactoryRoleEntity],
    ]: ...
