from core.security import create_access_token, verify_token
from domain.interfaces.services.token_service import ITokenService
from domain.value_objects.token_payload import TokenPayload


class TokenService(ITokenService):
    def __init__(self):
        pass

    def generate_token(self, payload: TokenPayload) -> str:
        return create_access_token(token_request=payload)

    def verify_token(self, token: str) -> TokenPayload:
        return verify_token(token=token)
