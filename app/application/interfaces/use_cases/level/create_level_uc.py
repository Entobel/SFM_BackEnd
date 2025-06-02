from abc import ABC, abstractmethod

from app.application.dto.level_dto import LevelDTO


class ICreateLevelUC(ABC):
    @abstractmethod
    def execute(self, level_dto: LevelDTO) -> bool:
        ...
