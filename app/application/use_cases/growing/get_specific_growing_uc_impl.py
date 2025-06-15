from app.application.interfaces.use_cases.zone.get_specific_growing_uc import IGetSpecificGrowingUC
from app.core.exception import NotFoundError
from app.domain.entities.zone_entity import ZoneEntity
from app.domain.interfaces.repositories.zone_repository import IZoneRepository


class GetSpecificGrowingUC(IGetSpecificGrowingUC):
    def __init__(self, zone_repo: IZoneRepository) -> None:
        self.zone_repo = zone_repo

    def execute(self, zone_id: int, growing_zone_status: int) -> int:
        query_entity = ZoneEntity(
            id=zone_id,
        )
        zone_entity = self.zone_repo.get_zone_by_id(zone_entity=query_entity)

        if not zone_entity:
            raise NotFoundError(f"Zone with ID {zone_id} not found.")

        growing_id = self.zone_repo.get_growing_by_zone_id(
            zone_id=zone_id, growing_zone_status=growing_zone_status)

        if not growing_id:
            raise NotFoundError(
                f"No growing found for zone ID {zone_id} with status {growing_zone_status}."
            )

        return growing_id
