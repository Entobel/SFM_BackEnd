from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.grinding_entity import GrindingEntity


class IGrindingRepository(ABC):
    @abstractmethod
    def get_grinding_by_id(
        self, grinding_entity: GrindingEntity
    ) -> Optional[GrindingEntity]:
        pass

    @abstractmethod
    def get_list_grinding_report(
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
        "items" : list[GrindingEntity],
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
    ]: ...

    @abstractmethod
    def get_grinding_by_name(
        self, grinding_entity: GrindingEntity
    ) -> Optional[GrindingEntity]:
        pass

    @abstractmethod
    def create_grinding(self, grinding_entity: GrindingEntity) -> bool:
        pass

    @abstractmethod
    def update_grinding(self, grinding_entity: GrindingEntity) -> GrindingEntity:
        pass

    @abstractmethod
    def delete_grinding_report(self, grinding_entity: GrindingEntity) -> GrindingEntity:
        pass
