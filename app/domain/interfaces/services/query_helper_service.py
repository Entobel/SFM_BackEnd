from abc import ABC, abstractmethod
from typing import Any, List, Optional, Tuple


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
    def add_search(self, cols: List[str], query: str) -> None: ...

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

    @abstractmethod
    def join_sql(self) -> str: ...

    @abstractmethod
    def add_table(self, table_name: str, _id: int): ...
