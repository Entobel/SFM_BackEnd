from core.exception import AuthenticationError
from domain.services.user_service import UserService
from domain.services.jwt_service import JWTService
from core.response import Response
from jose import JWTError
from core.error import handler


class GetMeUseCase:
    def __init__(self, user_service: UserService, jwt_service: JWTService):
        self.user_service = user_service
        self.jwt_service = jwt_service

    @handler
    def execute(self, token: str):
        payload_decoded = self.jwt_service.verify_token(token=token)

        user_id = payload_decoded.get("sub")

        self.user_service.get_user_by_id(id=user_id)
