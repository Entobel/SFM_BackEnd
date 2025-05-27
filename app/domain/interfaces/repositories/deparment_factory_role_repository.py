from abc import ABC, abstractmethod

from domain.entities.department_factory_role_entity import \
    DepartmentFactoryRoleEntity


class IDepartmentFactoryRoleRepository(ABC):
    @abstractmethod
    def check_department_factory_role_exists(
        self, department_factory_role_entity: DepartmentFactoryRoleEntity
    ) -> bool: ...

    @abstractmethod
    def get_department_factory_role_by_id(
        self, id: int
    ) -> DepartmentFactoryRoleEntity | None: ...

    @abstractmethod
    def create_department_factory_role(
        self,
        department_factory_role_entity: DepartmentFactoryRoleEntity,
    ) -> int: ...

    @abstractmethod
    def update_status_department_factory_role(
        self, department_factory_role_entity: DepartmentFactoryRoleEntity
    ) -> bool: ...

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
