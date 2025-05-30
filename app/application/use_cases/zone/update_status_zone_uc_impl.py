from application.dto.zone_dto import ZoneDTO
from application.interfaces.use_cases.zone.update_status_zone_uc import \
    IUpdateStatusZoneUC
from core.exception import BadRequestError
from domain.entities.zone_entity import ZoneEntity
from domain.interfaces.repositories.zone_repository import IZoneRepository


class UpdateStatusZoneUC(IUpdateStatusZoneUC):
    def __init__(self, zone_repo: IZoneRepository) -> None:
        self.zone_repo = zone_repo

    def execute(self, zone_dto: ZoneDTO) -> bool:
        query_entity = ZoneEntity(
            id=zone_dto.id,
            is_active=zone_dto.is_active,
        )

        zone_entity = self.zone_repo.get_zone_by_id(zone_entity=query_entity)

        if not zone_entity:
            raise BadRequestError("ETB_zone_khong_ton_tai")

        if zone_entity.is_active == query_entity.is_active:
            return True

        zone_entity.change_status(new_status=query_entity.is_active)

        is_success = self.zone_repo.update_status_zone(zone_entity=zone_entity)

        if not is_success:
            raise BadRequestError("ETB_cap_nhat_status_zone_khong_thanh_cong")

        return True
