from abc import ABC, abstractmethod
from typing import List

from domain.value_objects.access_policy import AccessPolicyContext


class IAccessPolicyService(ABC):
    @abstractmethod
    def is_accesible_with_role(
        self, role_id: int, resource: List[str] | str
    ) -> bool: ...

    @abstractmethod
    def is_accesible_with_department(
        self, source_department_id: int, target_department_id: int
    ) -> bool: ...

    @abstractmethod
    def is_accessible(
        self, access_ctx: AccessPolicyContext, allowed_role_ids: list[int] | None = None
    ) -> bool: ...

    @abstractmethod
    def _is_self(self, ctx: AccessPolicyContext) -> bool: ...

    @abstractmethod
    def _is_target_not_admin(self, ctx: AccessPolicyContext) -> bool: ...

    @abstractmethod
    def _is_admin(self, ctx: AccessPolicyContext) -> bool: ...

    @abstractmethod
    def _is_manager_in_same_department(self, ctx: AccessPolicyContext) -> bool: ...
