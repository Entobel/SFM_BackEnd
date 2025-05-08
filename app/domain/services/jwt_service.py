from core.security import create_access_token, verify_token
from schemas.security import TokenRequest
from jose import JWTError
from core.exception import BadRequestError


class JWTService:
    def __init__(self):
        pass

    def generate_token(self, token_request: TokenRequest) -> str:
        token = create_access_token(token_request=token_request)

        return token

    def verify_token(self, token: str) -> TokenRequest:

        try:
            payload = verify_token(token=token)

            return payload

        except JWTError as e:
            raise BadRequestError(error_code="ETB-123")
