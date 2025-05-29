from dataclasses import dataclass
from typing import Optional

# create table zone (
#     id serial not null,
#     zone_number int not null,
#     is_active bool default true,
#     created_at timestamptz default now(),
#     updated_at timestamptz default now(),

#     constraint pk_zone_id primary key (id)
# )


@dataclass
class ZoneEntity:
    id: Optional[int]
    zone_number: Optional[int]
    is_active: Optional[bool]

    def change_status(self, new_status: bool):
        self.is_active = new_status

    @classmethod
    def from_row(cls, row: dict) -> "ZoneEntity":
        return cls(
            id=row["z_id"],
            zone_number=row["z_zone_number"],
            is_active=row["z_is_active"],
        )
