from abc import ABC, abstractmethod


class IChangeStatusUC(ABC):
    @abstractmethod
    def execute(self, id: int, status: bool): ...
