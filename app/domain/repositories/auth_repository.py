from abc import ABC, abstractmethod


class IAuthRepository(ABC):

    @abstractmethod
    def get_user_by_phone(self, phone: str):
        pass

    @abstractmethod
    def get_user_by_email(self, email: str):
        pass
