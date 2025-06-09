from math import ceil
from typing import Any, List, Optional, Tuple

from dateutil.parser import isoparse

from app.core.exception import BadRequestError
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class QueryHelper(IQueryHelperService):
    def __init__(self):
        self.where_clauses: List[str] = []
        self.params: List[Any] = []
        self.join_clauses: List[str] = []
        self.tables: List[Any] = []

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

    def add_between_date(self, column: str, start_date: str, end_date: str):
        """Between date filter for timestamptz. Input: ISO 8601 strings from frontend."""
        start_dt = isoparse(start_date)
        end_dt = isoparse(end_date)

        self.where_clauses.append(f"{column} BETWEEN %s AND %s")
        self.params.extend([start_dt, end_dt])

    def add_between_value(
        self, column: str, lower_bound: int | float, upper_bound: int | float
    ) -> None:
        self.where_clauses.append(f"{column} BETWEEN %s AND %s")
        self.params.extend([lower_bound, upper_bound])

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

    def add_table(self, table_name: str, _id: int):
        abbr = self._get_abbr_table(table_name)

        join_fragment = (
            f"SELECT '{table_name}' AS name, "
            f"{abbr}.id AS found_id "
            f"FROM {table_name} {abbr} "
            f"WHERE {abbr}.id = %s"
        )
        self.join_clauses.append(join_fragment)
        self.params.append(_id)
        self.tables.append(table_name)

    def join_ids_sql(self) -> str:
        if not self.join_clauses:
            return ""
        return " UNION ALL ".join(self.join_clauses)

    def _get_abbr_table(self, name: str) -> str:
        return "".join(word[0] for word in name.split("_"))

    def verify_ids(self, targets: List[str], sources: List[str]):
        diff_keys = [item for item in sources if item not in targets]

        if len(diff_keys) > 0:
            for item in diff_keys:
                raise BadRequestError(f"ETB_{item}-khong-tim-thay")

    def all_tables(
        self,
    ) -> List[str]:
        return self.tables
