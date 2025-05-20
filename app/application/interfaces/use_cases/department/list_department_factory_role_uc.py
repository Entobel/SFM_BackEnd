from abc import ABC, abstractmethod

from domain.entities.department_factory_role_entity import DepartmentFactoryRoleEntity


class IListDepartmentFactoryRoleUC(ABC):
    @abstractmethod
    def execute(
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
