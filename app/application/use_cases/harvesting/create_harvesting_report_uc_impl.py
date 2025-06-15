from loguru import logger
from app.application.dto.harvesting_dto import HarvestingDTO
from app.application.dto.zone_level_dto import ZoneLevelDTO
from app.application.interfaces.use_cases.harvesting.create_harvesting_report_uc import ICreateHarvestingReportUC
from app.core.constants.common_enums import FormStatusEnum, HarvestZoneLevelStatusEnum, ZoneLevelStatusEnum
from app.core.exception import BadRequestError
from app.domain.entities.factory_entity import FactoryEntity
from app.domain.entities.harvesting_entity import HarvestingEntity
from app.domain.entities.harvesting_zone_level_entity import HarvestingZoneLevelEntity
from app.domain.entities.shift_entity import ShiftEntity
from app.domain.entities.user_entity import UserEntity
from app.domain.entities.zone_entity import ZoneEntity
from app.domain.entities.zone_level_entity import ZoneLevelEntity
from app.domain.interfaces.repositories.common_repository import ICommonRepository
from app.domain.interfaces.repositories.harvesting_repository import IHarvestingRepository
from app.domain.interfaces.repositories.zone_repository import IZoneRepository
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class CreateHarvestingReportUC(ICreateHarvestingReportUC):
    def __init__(
        self,
        harvesting_repo: IHarvestingRepository,
        zone_repo: IZoneRepository,
        query_helper: IQueryHelperService,
        common_repo: ICommonRepository,
    ) -> None:
        self.harvesting_repo = harvesting_repo
        self.zone_repo = zone_repo
        self.query_helper = query_helper
        self.common_repo = common_repo

    def execute(
        self,
        zone_id: int,
        harvesting_dto: HarvestingDTO,
        zone_level_dtos: list[ZoneLevelDTO],
    ) -> bool:
        harvesting_entity = self._create_harvesting_entity(
            harvesting_dto=harvesting_dto)

        requested_harvested_zone_level_ids = self._extract_zone_level_ids(
            zone_level_dtos=zone_level_dtos)

        if harvesting_dto.shift.id:
            self.query_helper.add_table(
                table_name="shifts", _id=harvesting_dto.shift.id)

        if zone_id:
            self.query_helper.add_table(table_name="zones", _id=zone_id)

        if harvesting_dto.factory.id:
            self.query_helper.add_table(
                table_name="factories", _id=harvesting_dto.factory.id
            )

        if harvesting_dto.created_by.id:
            self.query_helper.add_table(
                table_name="users", _id=harvesting_dto.created_by.id
            )

        if harvesting_dto.growing.id:
            self.query_helper.add_table(
                table_name="growings", _id=harvesting_dto.growing.id
            )

        join_sql = self.query_helper.join_ids_sql()

        ids_for_check = self.query_helper.all_params()

        result = self.common_repo.check_ids(sql=join_sql, ids=ids_for_check)

        self.query_helper.verify_ids(
            targets=[row[0] for row in result], sources=self.query_helper.all_tables()
        )

        available_zone_levels = self.zone_repo.get_list_zone_level_by_id(
            zone_id=zone_id, is_active=True, status=ZoneLevelStatusEnum.ON_GROWING.value
        )

        selected_zone_level_ids = [
            zone_level.id
            for zone_level in available_zone_levels
            if zone_level.id in requested_harvested_zone_level_ids
        ]

        list_harvesting_zone_level_entities = [
            HarvestingZoneLevelEntity(
                snapshot_level_name=zl.level.name,
                snapshot_zone_number=zl.zone.zone_number,
                zone_level=ZoneLevelEntity(
                    id=zl.id, zone=ZoneEntity(id=zl.zone.id)),
                status=HarvestZoneLevelStatusEnum.TEMPORARY.value,
            )
            for zl in available_zone_levels if zl.id in requested_harvested_zone_level_ids
        ]

        is_success = self.harvesting_repo.create_harvesting_report(
            harvesting_entity=harvesting_entity,
            list_harvesting_zone_level_entity=list_harvesting_zone_level_entities,
            zone_level_ids=selected_zone_level_ids
        )

        if not is_success:
            raise BadRequestError("ETB_loi_khi_tao_harvesting_report")

        return True

    def _create_harvesting_entity(self, harvesting_dto: HarvestingDTO) -> HarvestingEntity:
        """Create a HarvestingEntity from DTO with proper entity mapping."""
        logger.debug(f"Harvesting DTO: {harvesting_dto}")

        return HarvestingEntity(
            date_harvested=harvesting_dto.date_harvested,
            shift=ShiftEntity(id=harvesting_dto.shift.id),
            factory=FactoryEntity(id=harvesting_dto.factory.id),
            number_crates=harvesting_dto.number_crates,
            number_crates_discarded=harvesting_dto.number_crates_discarded,
            quantity_larvae=harvesting_dto.quantity_larvae,
            growing=harvesting_dto.growing,
            created_by=UserEntity(id=harvesting_dto.created_by.id),
            notes=harvesting_dto.notes,
            status=FormStatusEnum.PENDING.value
        )

    def _extract_zone_level_ids(self, zone_level_dtos: list[ZoneLevelDTO]) -> list[int]:
        """Extract zone level IDs from DTOs."""
        return [zone_level.id for zone_level in zone_level_dtos]
