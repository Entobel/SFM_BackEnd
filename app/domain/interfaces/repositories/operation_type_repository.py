from abc import ABC, abstractmethod

from app.domain.entities.operation_type_entity import OperationTypeEntity


class IOperationTypeRepository(ABC):
    @abstractmethod
    def get_all_operation_types(
        self,
        page: int,
        page_size: int,
        search: str,
        is_active: bool,
    ) -> dict[
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
        "items": list[OperationTypeEntity],
    ]: ...

    @abstractmethod
    def get_operation_type_by_name(
        self, name: str) -> OperationTypeEntity: ...

    @abstractmethod
    def get_operation_type_by_id(
        self, operation_type_entity: OperationTypeEntity
    ) -> OperationTypeEntity: ...

    @abstractmethod
    def create_operation_type(
        self, operation_type_entity: OperationTypeEntity
    ) -> bool: ...

    @abstractmethod
    def update_operation_type(
        self, operation_type_entity: OperationTypeEntity
    ) -> bool: ...

    @abstractmethod
    def update_status_operation_type(
        self, operation_type_entity: OperationTypeEntity
    ) -> bool: ...
