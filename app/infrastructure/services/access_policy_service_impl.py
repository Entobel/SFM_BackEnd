from app.core.exception import ForbiddenError
from app.domain.enums.role_enum import Role
from app.domain.interfaces.services.access_policy_service import \
    IAccessPolicyService
from app.domain.value_objects.access_policy import AccessPolicyContext


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

    def is_accessible(
        self,
        access_ctx: AccessPolicyContext,
        allowed_role_ids: list[int] | None = None,
    ) -> bool:
        """Determine whether *actor* can perform an action on *target*.

        When *allowed_role_ids* is provided, the check follows the new flow:

        1. Actor can always act on themselves.
        2. The actor's role **must** be in *allowed_role_ids*.
        3. The actor **cannot** perform the operation on a target that has the same
           role as themselves (even for admins).
        4. Admin-like roles (Role.get_admin_roles()) may operate across departments.
           Non-admin roles must belong to the **same** department as the target.

        If *allowed_role_ids* is *None*, the legacy behaviour is preserved to avoid
        breaking existing call-sites.
        """

        # Case 0: Actor performs action on themselves – always allowed.
        if access_ctx.target_user_id == access_ctx.actor_user_id:
            return True

        # -------------------- New flow (custom role list) --------------------
        if allowed_role_ids is not None:
            # 1. Actor role must be in the supplied whitelist.
            if access_ctx.actor_role_id not in allowed_role_ids:
                raise ForbiddenError(error_code="ETB-do_not_have_permission")

            # 2. Cannot operate on a user having the same role as actor.
            if access_ctx.actor_role_id == access_ctx.target_role_id:
                raise ForbiddenError(error_code="ETB-cannot_operate_on_same_role")

            # 3. Admin roles bypass the department check.
            if access_ctx.actor_role_id in Role.get_admin_roles():
                return True

            # 4. For non-admin roles, ensure the same department.
            if self.is_accesible_with_department(
                source_department_id=access_ctx.actor_department_id,
                target_department_id=access_ctx.target_department_id,
            ):
                return True

            raise ForbiddenError(error_code="ETB-do_not_have_permission")

        # -------------------- Legacy flow (no role list) --------------------
        # Case 1: Cannot operate on admin (unless it's self which is handled above).
        if access_ctx.target_role_id == Role.ADMIN.value:
            raise ForbiddenError(error_code="ETB-do_not_have_permission")

        # Case 2: Manager cannot operate on other managers.
        if (
            access_ctx.target_role_id == Role.MANAGER.value
            and access_ctx.actor_role_id == access_ctx.target_role_id
        ):
            raise ForbiddenError(
                error_code="ETB-cannot_set_for_manager_please_contact_admin"
            )

        # Case 3: Admin roles can operate freely (already filtered same-role above).
        if self.is_accesible_with_role(access_ctx.actor_role_id, "admin"):
            return True

        # Case 4: Managers may operate on users in the *same* department.
        if self.is_accesible_with_role(
            access_ctx.actor_role_id, "management"
        ) and self.is_accesible_with_department(
            source_department_id=access_ctx.actor_department_id,
            target_department_id=access_ctx.target_department_id,
        ):
            return True

        # Default deny.
        raise ForbiddenError(error_code="ETB-do_not_have_permission")

    def _is_self(self, access_ctx: AccessPolicyContext) -> bool:
        return access_ctx.actor_user_id == access_ctx.target_user_id

    def _is_target_not_admin(self, access_ctx: AccessPolicyContext) -> bool:
        return access_ctx.target_role_id != Role.ADMIN.value

    def _is_admin(self, access_ctx: AccessPolicyContext) -> bool:
        return self.is_accesible_with_role(access_ctx.actor_role_id, "admin")

    def _is_manager_in_same_department(self, access_ctx: AccessPolicyContext) -> bool:
        return self.is_accesible_with_role(
            access_ctx.actor_role_id, "management"
        ) and self.is_accesible_with_department(
            source_department_id=access_ctx.actor_department_id,
            target_department_id=access_ctx.target_department_id,
        )
