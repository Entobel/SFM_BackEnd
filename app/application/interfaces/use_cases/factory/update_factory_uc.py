from abc import ABC, abstractmethod

from application.schemas.factory_dto import FactoryDTO


class IUpdateFactoryUC(ABC):
    @abstractmethod
    def execute(self, factory_id: int, factory_dto: FactoryDTO) -> bool: ...
