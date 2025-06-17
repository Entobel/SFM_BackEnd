from abc import ABC, abstractmethod

from app.domain.entities.vfbd_entity import VfbdEntity


class IVfbdRepository(ABC):
    @abstractmethod
    def create_vfbd_report(self, vfbd_entity: VfbdEntity) -> bool: ...
