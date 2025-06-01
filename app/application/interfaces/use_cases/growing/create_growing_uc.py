from abc import ABC, abstractmethod

from app.presentation.schemas.growing_schema import CreateGrowingSchema


class ICreateGrowingUC(ABC):
    @abstractmethod
    def execute(self, body: CreateGrowingSchema): ...
