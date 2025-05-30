from abc import ABC, abstractmethod

from application.dto.diet_dto import DietDTO


class ICreateDietUC(ABC):
    @abstractmethod
    def execute(self, diet_dto: DietDTO) -> bool: ...
