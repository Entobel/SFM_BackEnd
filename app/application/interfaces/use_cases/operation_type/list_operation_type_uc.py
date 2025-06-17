from abc import ABC, abstractmethod

from app.domain.entities.operation_type_entity import OperationTypeEntity


class IListOperationTypeUC(ABC):
    @abstractmethod
    def execute(self, page: int,
                page_size: int,
                search: str,
                is_active: bool,) -> list[OperationTypeEntity]: ...
