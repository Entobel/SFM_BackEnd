from abc import ABC, abstractmethod

from app.domain.entities.dd_entity import DDEntity


class IDDRepository(ABC):
    @abstractmethod
    def create_dd_report(self, dd_entity: DDEntity) -> bool:
        """Create a new DD report."""
        pass
