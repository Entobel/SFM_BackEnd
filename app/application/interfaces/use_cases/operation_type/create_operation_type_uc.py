from abc import ABC, abstractmethod

from app.application.dto.operation_type_dto import OperationTypeDTO


class ICreateOperationTypeUC(ABC):
    @abstractmethod
    def execute(self, operation_type_dto: OperationTypeDTO) -> bool: ...
