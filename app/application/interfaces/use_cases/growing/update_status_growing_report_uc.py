from abc import ABC, abstractmethod


class IUpdateStatusGrowingReportUC(ABC):
    @abstractmethod
    def execute(
        self,
        status: int,
        rejected_at: str,
        growing_id: int,
        rejected_by: int,
        rejected_reason: str,
        approved_at: str,
        approved_by: int,
    ): ...
