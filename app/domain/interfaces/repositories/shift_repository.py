from domain.entities.shift_entity import ShiftEntity
from abc import ABC, abstractmethod


class IShiftRepository(ABC):
    @abstractmethod
    def get_all_shifts(self) -> list[ShiftEntity]: ...
