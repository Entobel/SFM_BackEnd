from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.grinding_entity import GrindingEntity


class IGrindingRepository(ABC):
    @abstractmethod
    def get_grinding_by_id(self, grinding_entity: GrindingEntity) -> Optional[GrindingEntity]:
        pass

    @abstractmethod
    def get_grinding_by_name(self, grinding_entity: GrindingEntity) -> Optional[GrindingEntity]:
        pass

    @abstractmethod
    def create_grinding(self, grinding_entity: GrindingEntity) -> bool:
        pass

    @abstractmethod
    def update_grinding(self, grinding_entity: GrindingEntity) -> GrindingEntity:
        pass

    @abstractmethod
    def update_status_grinding(self, grinding_entity: GrindingEntity) -> GrindingEntity:
        pass
