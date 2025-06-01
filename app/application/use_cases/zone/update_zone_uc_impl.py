from app.application.dto.zone_dto import ZoneDTO
from app.application.interfaces.use_cases.zone.update_zone_uc import IUpdateZoneUC
from app.core.exception import BadRequestError
from app.domain.entities.zone_entity import ZoneEntity
from app.domain.interfaces.repositories.zone_repository import IZoneRepository


class UpdateZoneUC(IUpdateZoneUC):
    def __init__(self, zone_repo: IZoneRepository) -> None:
        self.zone_repo = zone_repo

    def execute(self, zone_dto: ZoneDTO) -> bool:
        query_entity = ZoneEntity(
            id=zone_dto.id,
            zone_number=zone_dto.zone_number,
            is_active=zone_dto.is_active,
        )

        zone_entity = self.zone_repo.get_zone_by_id(zone_entity=query_entity)

        if not zone_entity:
            raise BadRequestError("ETB_zone_khong_ton_tai")

        # Check existed
        is_exist_zone = self.zone_repo.get_zone_by_zone_number(zone_entity=query_entity)

        if is_exist_zone:
            raise BadRequestError("ETB_zone_da_ton_tai")

        zone_entity.update_zone(new_zone_number=query_entity.zone_number)

        # Update zone
        is_success = self.zone_repo.update_zone(zone_entity=zone_entity)

        if not is_success:
            raise BadRequestError("ETB_cap_nhat_zone_khong_thanh_cong")

        return True
