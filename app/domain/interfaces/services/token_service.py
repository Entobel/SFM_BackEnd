from abc import ABC, abstractmethod

from domain.value_objects.token_payload import TokenPayload


class ITokenService(ABC):
    @abstractmethod
    def generate_token(self, payload: TokenPayload) -> str: ...

    @abstractmethod
    def verify_token(self, token: str) -> TokenPayload: ...
