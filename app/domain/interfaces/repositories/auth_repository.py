from abc import ABC, abstractmethod


class IAuthRepository(ABC):

    @abstractmethod
    def get_user_by_email_or_phone(self, username: str): ...
