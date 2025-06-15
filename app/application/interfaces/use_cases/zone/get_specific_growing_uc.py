from abc import ABC, abstractmethod


class IGetSpecificGrowingUC(ABC):
    @abstractmethod
    def execute(self, zone_id: int, growing_zone_status: int) -> int:
        ...
