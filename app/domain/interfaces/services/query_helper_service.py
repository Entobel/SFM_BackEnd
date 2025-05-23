from typing import Any, List, Optional, Tuple
from abc import ABC, abstractmethod


class IQueryHelperService(ABC):
    @abstractmethod
    def add_eq(self, column: str, value: Any):
        pass

    @abstractmethod
    def add_fulltext(self, cols: List[str], query: str, dictionary: str = "english"):
        pass

    @abstractmethod
    def where_sql(self) -> str:
        pass

    @abstractmethod
    def paginate(self, page: int, page_size: int) -> Tuple[str, List[Any]]:
        pass

    @abstractmethod
    def total_pages(self, total: int, page_size: int) -> int:
        pass

    @abstractmethod
    def all_params(self, extra: List[Any] = None) -> List[Any]:
        pass

    @abstractmethod
    def add_bool(
        self,
        column: str,
        flag: Optional[bool],
    ): ...
