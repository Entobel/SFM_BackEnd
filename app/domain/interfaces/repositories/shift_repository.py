from abc import ABC, abstractmethod

from domain.entities.shift_entity import ShiftEntity


class IShiftRepository(ABC):
    @abstractmethod
    def get_shift_by_id(self, id: int) -> ShiftEntity | None: ...

    @abstractmethod
    def get_shift_by_name(self, name: str) -> ShiftEntity | None: ...

    @abstractmethod
    def update_status_shift(self, shift_entity: ShiftEntity) -> bool: ...

    @abstractmethod
    def update_shift(self, shift_entity: ShiftEntity) -> bool: ...

    @abstractmethod
    def get_all_shifts(self) -> list[ShiftEntity]: ...
