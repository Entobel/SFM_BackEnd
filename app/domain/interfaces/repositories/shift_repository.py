from domain.entities.shift_entity import ShiftEntity
from abc import ABC, abstractmethod


class IShiftRepository(ABC):
    @abstractmethod
    def get_shift_by_id(self, id: int) -> ShiftEntity: ...

    @abstractmethod
    def get_shift_by_name(self, name: str) -> ShiftEntity: ...

    @abstractmethod
    def update_status_shift(self, shift_entity: ShiftEntity) -> bool: ...

    @abstractmethod
    def update_shift(self, shift_entity: ShiftEntity) -> bool: ...

    @abstractmethod
    def get_all_shifts(self) -> list[ShiftEntity]: ...
