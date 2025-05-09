from abc import ABC, abstractmethod


class IPasswordService(ABC):

    @abstractmethod
    def hash_password(self, password: str) -> str: ...

    @abstractmethod
    def verify_password(self, owned_password: str, raw_password: str) -> bool: ...
