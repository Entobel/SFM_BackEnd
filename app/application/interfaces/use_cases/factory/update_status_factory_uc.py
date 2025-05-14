from abc import ABC, abstractmethod


class IUpdateStatusFactoryUC(ABC):
    @abstractmethod
    def execute(self, factory_id: int, is_active: bool) -> bool: ...
