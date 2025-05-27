from abc import ABC, abstractmethod
from typing import Any, List, Optional, Tuple


class ICursorQueryHelperService(ABC):
    @abstractmethod
    def add_eq(self, column: str, value: Any) -> None: ...

    @abstractmethod
    def add_search(self, cols: List[str], query: str) -> None: ...

    @abstractmethod
    def add_bool(self, column: str, flag: Optional[bool]) -> None: ...

    @abstractmethod
    def add_cursor(
        self, column: str, cursor: Optional[Any], direction: str = "after"
    ): ...

    @abstractmethod
    def where_sql(self) -> str: ...

    @abstractmethod
    def limit_sql(self, page_size: int) -> Tuple[str, List[Any]]: ...

    @abstractmethod
    def all_params(self, extra: List[Any] = None) -> List[Any]: ...
