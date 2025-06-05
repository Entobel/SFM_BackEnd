from abc import ABC, abstractmethod

from app.domain.entities.growing_entity import GrowingEntity
from app.domain.entities.growing_zone_level_entity import GrowingZoneLevelEntity


class IGrowingRepository(ABC):
    @abstractmethod
    def create_growing_report(
        self,
        growing_entity: GrowingEntity,
        zone_level_ids: list[int],
        list_growing_zone_level_entity: list[GrowingZoneLevelEntity],
    ): ...
