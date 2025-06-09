from app.application.dto.growing_dto import GrowingDTO
from app.application.dto.zone_level_dto import ZoneLevelDTO
from loguru import logger

from app.application.interfaces.use_cases.growing.create_growing_report_uc import (
    ICreateGrowingReportUC,
)
from app.core.exception import BadRequestError
from app.domain.entities.diet_entity import DietEntity
from app.domain.entities.factory_entity import FactoryEntity
from app.domain.entities.growing_entity import GrowingEntity
from app.domain.entities.growing_zone_level_entity import GrowingZoneLevelEntity
from app.domain.entities.production_object_entity import ProductionObjectEntity
from app.domain.entities.production_type_entity import ProductionTypeEntity
from app.domain.entities.shift_entity import ShiftEntity
from app.domain.entities.user_entity import UserEntity
from app.domain.entities.zone_entity import ZoneEntity
from app.domain.entities.zone_level_entity import ZoneLevelEntity
from app.domain.interfaces.repositories.common_repository import ICommonRepository
from app.domain.interfaces.repositories.diet_repository import IDietRepository
from app.domain.interfaces.repositories.factory_repository import IFactoryRepository
from app.domain.interfaces.repositories.growing_repository import IGrowingRepository
from app.domain.interfaces.repositories.production_object_repository import (
    IProductionObjectRepository,
)
from app.domain.interfaces.repositories.production_type_repository import (
    IProductionTypeRepository,
)
from app.domain.interfaces.repositories.shift_repository import IShiftRepository
from app.domain.interfaces.repositories.user_repository import IUserRepository
from app.domain.interfaces.repositories.zone_repository import IZoneRepository
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class CreateGrowingReportUC(ICreateGrowingReportUC):
    def __init__(
        self,
        growing_repo: IGrowingRepository,
        zone_repo: IZoneRepository,
        query_helper: IQueryHelperService,
        common_repo: ICommonRepository,
    ) -> None:
        self.growing_repo = growing_repo
        self.zone_repo = zone_repo
        self.query_helper = query_helper
        self.common_repo = common_repo

    def execute(
        self,
        zone_id: int,
        growing_dto: GrowingDTO,
        zone_level_dtos: list[ZoneLevelDTO],
    ) -> bool:
        growing_entity = self._create_growing_entity(growing_dto)
        requested_zone_level_ids = self._extract_zone_level_ids(zone_level_dtos)

        if growing_dto.shift.id:
            self.query_helper.add_table(table_name="shifts", _id=growing_dto.shift.id)

        if zone_id:
            self.query_helper.add_table(table_name="zones", _id=zone_id)

        if growing_dto.production_object.id:
            self.query_helper.add_table(
                table_name="production_objects", _id=growing_dto.production_object.id
            )

        if growing_dto.production_type.id:
            self.query_helper.add_table(
                table_name="production_types", _id=growing_dto.production_type.id
            )

        if growing_dto.diet.id:
            self.query_helper.add_table(table_name="diets", _id=growing_dto.diet.id)

        if growing_dto.factory.id:
            self.query_helper.add_table(
                table_name="factories", _id=growing_dto.factory.id
            )

        if growing_dto.user.id:
            self.query_helper.add_table(table_name="users", _id=growing_dto.user.id)

        join_sql = self.query_helper.join_ids_sql()
        ids_for_check = self.query_helper.all_params()

        result = self.common_repo.check_ids(sql=join_sql, ids=ids_for_check)

        self.query_helper.verify_ids(
            targets=[row[0] for row in result], sources=self.query_helper.all_tables()
        )

        # Get vailable zone level for zone_id
        available_zone_levels = self.zone_repo.get_list_zone_level_by_id(
            zone_id=zone_id, is_active=True, is_used=False
        )

        if not available_zone_levels:
            raise BadRequestError("ETB_khong_con_zone_level_nao_hop_le")

        available_zone_level_ids = {level.id for level in available_zone_levels}

        invalid_zone_level_ids = (
            set(requested_zone_level_ids) - available_zone_level_ids
        )

        if invalid_zone_level_ids:
            raise BadRequestError(
                f"ETB_zone_da_duoc_su_dung, các zone_level_id không hợp lệ: {(invalid_zone_level_ids)}"
            )

        selected_zone_level_ids = [
            zone_level.id
            for zone_level in available_zone_levels
            if zone_level.id in requested_zone_level_ids
        ]

        list_growing_zone_level = [
            GrowingZoneLevelEntity(
                snapshot_level_name=zl.level.name,
                snapshot_zone_number=zl.zone.zone_number,
                zone_level=ZoneLevelEntity(id=zl.id),
                is_assigned=zl.id in requested_zone_level_ids,
            )
            for zl in available_zone_levels
        ]

        is_success = self.growing_repo.create_growing_report(
            growing_entity=growing_entity,
            list_growing_zone_level_entity=list_growing_zone_level,
            zone_level_ids=selected_zone_level_ids,
        )

        if not is_success:
            raise BadRequestError("ETB_loi_khi_tao")

        return True

    def _create_growing_entity(self, growing_dto: GrowingDTO) -> GrowingEntity:
        """Create a GrowingEntity from DTO with proper entity mapping."""

        return GrowingEntity(
            date_produced=growing_dto.date_produced,
            shift=ShiftEntity(id=growing_dto.shift.id),
            production_object=ProductionObjectEntity(
                id=growing_dto.production_object.id
            ),
            production_type=ProductionTypeEntity(id=growing_dto.production_type.id),
            diet=DietEntity(id=growing_dto.diet.id),
            factory=FactoryEntity(id=growing_dto.factory.id),
            number_crates=growing_dto.number_crates,
            substrate_moisture=growing_dto.substrate_moisture,
            created_by=UserEntity(id=growing_dto.user.id),
            notes=growing_dto.notes,
        )

    def _extract_zone_level_ids(self, zone_level_dtos: list[ZoneLevelDTO]) -> list[int]:
        """Extract zone level IDs from DTOs."""
        return [zone_level.id for zone_level in zone_level_dtos]
