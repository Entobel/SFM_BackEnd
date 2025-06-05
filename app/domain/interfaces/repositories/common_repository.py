from abc import ABC, abstractmethod


class ICommonRepository(ABC):
    @abstractmethod
    def check_ids(self, sql: str, ids: list[int]) -> list[tuple[str, int]]:
        pass
