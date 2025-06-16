from app.application.interfaces.use_cases.zone.list_zone_uc import IListZoneUC
from app.domain.entities.zone_entity import ZoneEntity
from app.domain.interfaces.repositories.zone_repository import IZoneRepository


class ListZoneUC(IListZoneUC):
    def __init__(self, zone_repo: IZoneRepository) -> None:
        self.zone_repo = zone_repo

    def execute(
        self, page: int, page_size: int, search: str, is_active: bool, factory_id: int
    ) -> dict[
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
        "items": list[ZoneEntity],
    ]:
        return self.zone_repo.get_list_zones(
            page=page,
            page_size=page_size,
            search=search,
            is_active=is_active,
            factory_id=factory_id,
        )
