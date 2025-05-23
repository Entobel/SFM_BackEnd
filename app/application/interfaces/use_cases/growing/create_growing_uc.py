from presentation.schemas.growing_dto import CreateGrowingDTO
from abc import ABC, abstractmethod


class ICreateGrowingUC(ABC):
    @abstractmethod
    def execute(self, body: CreateGrowingDTO): ...
