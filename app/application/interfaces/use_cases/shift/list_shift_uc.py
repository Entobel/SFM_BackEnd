from domain.interfaces.repositories.shift_repository import IShiftRepository
from domain.entities.shift_entity import ShiftEntity
from abc import ABC, abstractmethod


class IListShiftUC(ABC):
    @abstractmethod
    def execute(self) -> list[ShiftEntity]: ...
