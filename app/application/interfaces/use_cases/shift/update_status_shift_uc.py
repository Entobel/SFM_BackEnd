from abc import ABC, abstractmethod

from application.schemas.shift_dto import ShiftDTO


class IUpdateStatusShiftUC(ABC):
    @abstractmethod
    def execute(self, shift_dto: ShiftDTO) -> bool: ...
