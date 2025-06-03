from app.application.interfaces.use_cases.zone.list_zone_level_uc import (
    IListZoneLevelUC,
)
from app.domain.entities.zone_level_entity import ZoneLevelEntity
from app.domain.interfaces.repositories.zone_repository import IZoneRepository


class ListZoneLevelUC(IListZoneLevelUC):
    def __init__(self, repo: IZoneRepository):
        self.repo = repo

    def execute(
        self, page: int, page_size: int, search: str, zone_id: int, is_active: bool
    ) -> dict[
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
        "items" : list[ZoneLevelEntity],
    ]:
        return self.repo.get_list_zone_levels(
            page=page,
            page_size=page_size,
            search=search,
            zone_id=zone_id,
            is_active=is_active,
        )
