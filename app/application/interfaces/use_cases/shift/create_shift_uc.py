from abc import ABC, abstractmethod

from application.schemas.shift_schemas import ShiftDTO


class ICreateShiftUC(ABC):
    @abstractmethod
    def execute(self, shift_dto: ShiftDTO) -> bool: ...
