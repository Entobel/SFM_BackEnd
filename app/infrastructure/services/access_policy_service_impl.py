from core.exception import ForbiddenError
from domain.value_objects.access_policy import AccessPolicyContext
from domain.enums.role_enum import Role
from domain.interfaces.services.access_policy_service import IAccessPolicyService


class AccessPolicyService(IAccessPolicyService):
    def __init__(self) -> None:
        super().__init__()

    def is_accesible_with_role(self, role_id: int, required_access_level: str) -> bool:
        if required_access_level == "admin":
            return role_id in Role.get_admin_roles()
        elif required_access_level == "management":
            return role_id in Role.get_management_roles()
        return False

    def is_accesible_with_department(
        self, source_department_id: int, target_department_id: int
    ) -> bool:
        return source_department_id == target_department_id

    def is_accessible(self, ctx: AccessPolicyContext) -> bool:
        # Case 1: Do by yourself
        if ctx.target_user_id == ctx.actor_user_id:
            return True

        # Case 2: Cannot do for admin
        if ctx.target_role_id == 1:
            raise ForbiddenError(error_code="ETB-do_not_have_permission")

        if ctx.target_role_id == 2 and ctx.actor_role_id == ctx.target_role_id:
            raise ForbiddenError(
                error_code="ETB-cannot_set_for_manager_please_contact_admin"
            )

        # Case 3: Do by admin
        if self.is_accesible_with_role(ctx.actor_role_id, "admin"):
            return True

        # Case 4: Update only for same department by manager
        if self.is_accesible_with_role(
            ctx.actor_role_id, "management"
        ) and self.is_accesible_with_department(
            source_department_id=ctx.actor_department_id,
            target_department_id=ctx.target_department_id,
        ):
            return True
        else:
            raise ForbiddenError(error_code="ETB-do_not_have_permission")

    def _is_self(self, ctx: AccessPolicyContext) -> bool:
        return ctx.actor_user_id == ctx.target_user_id

    def _is_target_not_admin(self, ctx: AccessPolicyContext) -> bool:
        return ctx.target_role_id != Role.ADMIN.value

    def _is_admin(self, ctx: AccessPolicyContext) -> bool:
        return self.is_accesible_with_role(ctx.actor_role_id, "admin")

    def _is_manager_in_same_department(self, ctx: AccessPolicyContext) -> bool:
        return self.is_accesible_with_role(
            ctx.actor_role_id, "management"
        ) and self.is_accesible_with_department(
            source_department_id=ctx.actor_department_id,
            target_department_id=ctx.target_department_id,
        )
