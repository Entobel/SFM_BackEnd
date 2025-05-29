from abc import ABC, abstractmethod


class ICreateZoneUC(ABC):

    @abstractmethod
    def execute(self): ...
