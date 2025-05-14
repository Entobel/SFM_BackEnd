from math import ceil
from typing import Any, List, Optional, Tuple

from domain.interfaces.services.query_helper_service import IQueryHelperService


class QueryHelper(IQueryHelperService):
    def __init__(self):
        self.where_clauses: List[str] = []
        self.params: List[Any] = []

    def add_eq(self, column: str, value: Any):
        """= filter"""
        self.where_clauses.append(f"{column} = %s")
        self.params.append(value)

    def add_fulltext(self, cols: List[str], query: str, dictionary: str = "english"):
        """Postgres full-text over multiple columns"""
        tsv = " || ' ' || ".join(cols)
        self.where_clauses.append(
            f"to_tsvector('{dictionary}', {tsv}) @@ plainto_tsquery('{dictionary}', %s)"
        )
        self.params.append(query)

    def add_search(self, cols: List[str], query: str):
        """Substring search using ILIKE on multiple columns"""
        pattern = f"%{query}%"
        ilike_clauses = [f"{col} ILIKE %s" for col in cols]
        self.where_clauses.append("(" + " OR ".join(ilike_clauses) + ")")
        self.params.extend([pattern] * len(cols))

    def where_sql(self) -> str:
        if not self.where_clauses:
            return ""
        return "WHERE " + " AND ".join(self.where_clauses)

    def paginate(self, page: int, page_size: int) -> Tuple[str, List[Any]]:
        total_offset = (page - 1) * page_size
        return "LIMIT %s OFFSET %s", [page_size, total_offset]

    def total_pages(self, total: int, page_size: int) -> int:
        return ceil(total / page_size) if total else 1

    def all_params(self, extra: List[Any] = None) -> List[Any]:
        return self.params + (extra or [])

    def add_bool(
        self,
        column: str,
        flag: Optional[bool],
    ):
        """Nếu flag=None → skip; nếu flag=True/False → filter column = flag"""
        if flag is not None:
            self.where_clauses.append(f"{column} = %s")
            self.params.append(flag)
