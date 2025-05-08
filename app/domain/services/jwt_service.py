from core.security import create_access_token
from schemas.security import TokenRequest


class JWTService:
    def __init__(self):
        pass

    def generate_token(self, token_request: TokenRequest) -> str:
        token = create_access_token(token_request=token_request)

        return token
