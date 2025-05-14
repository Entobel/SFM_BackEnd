from abc import ABC, abstractmethod


class IDepartmentFactoryRoleRepository(ABC):
    @abstractmethod
    def check_department_factory_role_exists(
        self, department_id: int, factory_id: int, role_id: int
    ) -> bool: ...

    @abstractmethod
    def create_department_factory_role(
        self, department_id: int, factory_id: int, role_id: int
    ) -> int: ...
