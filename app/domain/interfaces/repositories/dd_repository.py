from abc import ABC, abstractmethod

from app.domain.entities.dd_entity import DdEntity


class IDdRepository(ABC):

    @abstractmethod
    def get_dd_report_by_id(self, dd_entity: DdEntity) -> DdEntity | None: ...

    @abstractmethod
    def update_dd_report(self, dd_entity: DdEntity) -> bool: ...

    @abstractmethod
    def get_list_dd_report(
        self,
        page: int,
        page_size: int,
        search: str,
        factory_id: int | None,
        start_date: str | None,
        end_date: str | None,
        report_status: int | None,
        is_active: bool | None,
    ) -> dict[
        "items" : list[DdEntity],
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
    ]: ...

    @abstractmethod
    def create_dd_report(self, dd_entity: DdEntity) -> bool:
        """Create a new DD report."""
        pass

    @abstractmethod
    def delete_dd_report(self, dd_entity: DdEntity) -> bool: ...
