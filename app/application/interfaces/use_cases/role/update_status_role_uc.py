from abc import ABC, abstractmethod


class IUpdateStatusRoleUC(ABC):
    @abstractmethod
    def execute(self, role_id: int, is_active: bool): ...
