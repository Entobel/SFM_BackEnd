from app.application.dto.zone_dto import ZoneDTO
from app.application.interfaces.use_cases.zone.create_zone_uc import ICreateZoneUC
from app.core.exception import BadRequestError
from app.domain.entities.zone_entity import ZoneEntity
from app.domain.interfaces.repositories.zone_repository import IZoneRepository


class CreateZoneUC(ICreateZoneUC):
    def __init__(self, zone_repo: IZoneRepository) -> None:
        self.zone_repo = zone_repo

    def execute(self, zone_dto: ZoneDTO):
        zone_entity = ZoneEntity(zone_number=zone_dto.zone_number)

        is_exist_zone = self.zone_repo.get_zone_by_zone_number(zone_entity=zone_entity)

        # Check existed
        if is_exist_zone:
            raise BadRequestError("ETB_zone_da_ton_tai")

        is_success = self.zone_repo.create_zone(zone_entity=zone_entity)

        if not is_success:
            raise BadRequestError("ETB_tao_zon_khong_thanh_cong")

        return True
