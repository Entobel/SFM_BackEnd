from abc import ABC, abstractmethod


class IUserRepository(ABC):
    @abstractmethod
    def get_user_profile_by_id(id: int):
        pass

    @abstractmethod
    def get_user_by_email_or_phone(self, username: str):
        pass
