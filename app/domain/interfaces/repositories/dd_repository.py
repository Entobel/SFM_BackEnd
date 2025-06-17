from abc import ABC, abstractmethod

from app.domain.entities.dd_entity import DdEntity


class IDdRepository(ABC):
    @abstractmethod
    def create_dd_report(self, dd_entity: DdEntity) -> bool:
        """Create a new DD report."""
        pass
