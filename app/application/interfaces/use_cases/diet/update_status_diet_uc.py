from abc import ABC, abstractmethod

from application.schemas.diet_dto import DietDTO


class IUpdateStatusDietUC(ABC):
    @abstractmethod
    def execute(self, diet_dto: DietDTO) -> bool: ...
