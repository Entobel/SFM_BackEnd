from abc import ABC, abstractmethod

from presentation.schemas.growing_dto import CreateGrowingDTO


class ICreateGrowingUC(ABC):
    @abstractmethod
    def execute(self, body: CreateGrowingDTO): ...
