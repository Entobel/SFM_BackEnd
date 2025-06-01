from abc import ABC, abstractmethod

from app.domain.entities.factory_entity import FactoryEntity


class ICreateFactoryUC(ABC):
    @abstractmethod
    def execute(self, factory: FactoryEntity) -> bool: ...
