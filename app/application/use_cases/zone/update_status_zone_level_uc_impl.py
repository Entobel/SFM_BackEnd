from app.application.interfaces.use_cases.zone.update_status_zone_level_uc import (
    IUpdateStatusZoneLevelUC,
)
from app.application.dto.zone_level_dto import ZoneLevelDTO
from app.core.exception import BadRequestError
from app.domain.entities.zone_level_entity import ZoneLevelEntity
from app.domain.interfaces.repositories.zone_repository import IZoneRepository


class UpdateStatusZoneLevelUC(IUpdateStatusZoneLevelUC):
    def __init__(self, repo: IZoneRepository):
        self.repo = repo

    def execute(self, zone_level_dto: ZoneLevelDTO):
        query_entity = ZoneLevelEntity(
            id=zone_level_dto.id,
            is_active=zone_level_dto.is_active,
        )

        # check existed
        zone_level_entity = self.repo.get_zone_level_by_id(query_entity)

        if zone_level_entity is None:
            raise BadRequestError("ETB-khong_tim_thay_zone_level")

        if zone_level_entity.is_active == query_entity.is_active:
            return True

        zone_level_entity.change_is_active(query_entity.is_active)

        is_success = self.repo.update_status_zone_level(
            zone_level_entity=zone_level_entity
        )

        if not is_success:
            raise BadRequestError("ETB-thay_doi_status_zone_level_khong_thanh_cong")

        return True
