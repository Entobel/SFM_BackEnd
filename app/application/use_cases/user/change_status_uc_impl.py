from application.interfaces.use_cases.user.change_status_uc import IChangeStatusUC
from domain.services.user_service import UserService
from domain.interfaces.services.access_policy_service import IAccessPolicyService


class ChangeStatusUC(IChangeStatusUC):
    def __init__(
        self, user_service: UserService, access_policy_service: IAccessPolicyService
    ) -> None:
        self.user_service = user_service
        self.access_policy_service = access_policy_service

        super().__init__()

    def execute(self, id: int, status: bool):

        self.user_service.change_status(status=status, user=user)
