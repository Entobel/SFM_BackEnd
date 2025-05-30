from abc import ABC, abstractmethod

from presentation.schemas.growing_schema import CreateGrowingSchema


class ICreateGrowingUC(ABC):
    @abstractmethod
    def execute(self, body: CreateGrowingSchema): ...
