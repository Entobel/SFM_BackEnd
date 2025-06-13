from abc import ABC, abstractmethod

from app.application.dto.growing_dto import UpdateGrowingDTO

class IUpdateGrowingReportUC(ABC):
    @abstractmethod
    def execute(self, growing_dto: UpdateGrowingDTO, new_zone_level_ids: list[int], old_zone_level_ids: list[int], new_zone_id: int,old_zone_id: int):...