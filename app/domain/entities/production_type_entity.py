from dataclasses import dataclass


@dataclass
class ProductionTypeEntity:
    id: int
    name: str
    abbr_name: str
    description: str
    is_active: bool

    @classmethod
    def from_row(cls, row: dict) -> "ProductionTypeEntity":
        return cls(
            id=row["pt_id"],
            name=row["pt_name"],
            abbr_name=row["pt_abbr_name"],
            description=row["pt_description"],
            is_active=row["pt_is_active"],
        )
