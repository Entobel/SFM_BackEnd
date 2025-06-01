from typing import Any, List, Optional, Tuple

from app.domain.interfaces.services.cursor_query_helper import \
    ICursorQueryHelperService


class CursorQueryHelperService(ICursorQueryHelperService):
    def __init__(self):
        self.where_clauses: List[str] = []
        self.params: List[Any] = []

    def add_eq(self, column: str, value: Any):
        self.where_clauses.append(f"{column} = %s")
        self.params.append(value)

    def add_search(self, cols: List[str], query: str):
        pattern = f"%{query}%"
        ilike_clauses = [f"{col} ILIKE %s" for col in cols]
        self.where_clauses.append("(" + " OR ".join(ilike_clauses) + ")")
        self.params.extend([pattern] * len(cols))

    def add_bool(self, column: str, flag: Optional[bool]):
        if flag is not None:
            self.where_clauses.append(f"{column} = %s")
            self.params.append(flag)

    def add_cursor(self, column: str, cursor: Optional[Any], direction: str = "after"):
        if cursor is not None:
            op = ">" if direction == "after" else "<"
            self.where_clauses.append(f"{column} {op} %s")
            self.params.append(cursor)

    def where_sql(self) -> str:
        if not self.where_clauses:
            return ""
        return "WHERE " + " AND ".join(self.where_clauses)

    def limit_sql(self, page_size: int) -> Tuple[str, List[Any]]:
        return "LIMIT %s", [page_size]

    def all_params(self, extra: List[Any] = None) -> List[Any]:
        return self.params + (extra or [])
