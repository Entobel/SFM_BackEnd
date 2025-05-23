from abc import ABC, abstractmethod

from application.schemas.diet_schemas import DietDTO


class IUpdateDietUC(ABC):
    @abstractmethod
    def execute(self, diet_dto: DietDTO) -> bool: ...
