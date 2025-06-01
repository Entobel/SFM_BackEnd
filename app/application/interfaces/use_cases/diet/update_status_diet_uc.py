from abc import ABC, abstractmethod

from app.application.dto.diet_dto import DietDTO


class IUpdateStatusDietUC(ABC):
    @abstractmethod
    def execute(self, diet_dto: DietDTO) -> bool: ...
