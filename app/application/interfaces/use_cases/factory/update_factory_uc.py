from abc import ABC, abstractmethod

from app.application.dto.factory_dto import FactoryDTO


class IUpdateFactoryUC(ABC):
    @abstractmethod
    def execute(self, factory_id: int, factory_dto: FactoryDTO) -> bool: ...
