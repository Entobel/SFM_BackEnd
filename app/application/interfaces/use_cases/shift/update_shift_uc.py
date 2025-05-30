from abc import ABC, abstractmethod

from application.dto.shift_dto import ShiftDTO


class IUpdateShiftUC(ABC):
    @abstractmethod
    def execute(self, shift_dto: ShiftDTO) -> bool: ...
