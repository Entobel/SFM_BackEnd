from domain.services.user_service import UserService
from domain.interfaces.services.access_policy_service import IAccessPolicyService
from application.interfaces.use_cases.user.change_password_uc import IChangePasswordUC
from core.exception import ForbiddenError
from domain.entities.user_entity import UserEntity


class ChangePasswordUC(IChangePasswordUC):
    def __init__(
        self, user_service: UserService, access_policy_service: IAccessPolicyService
    ):
        self.user_service = user_service
        self.access_policy_service = access_policy_service

    def execute(
        self,
        target_user: UserEntity,
        actor_user_id: int,
        old_password: str,
        new_password: str,
    ) -> bool:
        # Business rule: if not self-changing password, old_password is not required
        # (because managers / admins may reset subordinate passwords).
        # Validation of permission has already been handled by the AccessCheckDep.

        # Ensure the actor is either the owner of the account or has provided the
        # old password when required.
        is_self_change = target_user.id == actor_user_id

        if is_self_change and not old_password:
            raise ForbiddenError(error_code="ETB-khongdungmatkhaucu")

        self.user_service.change_password(
            user=target_user, old_password=old_password, new_password=new_password
        )

        return True
