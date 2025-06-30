from re import I, S
from loguru import logger
from app.application.dto.harvesting_dto import HarvestingDTO
from app.application.interfaces.use_cases.harvesting.update_harvesting_report_uc import (
    IUpdateHarvestingReportUC,
)
from app.core.constants.common_enums import FormStatusEnum
from app.core.exception import BadRequestError
from app.domain.entities.diet_entity import DietEntity
from app.domain.entities.factory_entity import FactoryEntity
from app.domain.entities.growing_entity import GrowingEntity
from app.domain.entities.harvesting_entity import HarvestingEntity
from app.domain.entities.product_type_entity import ProductTypeEntity
from app.domain.entities.operation_type_entity import OperationTypeEntity
from app.domain.entities.shift_entity import ShiftEntity
from app.domain.entities.user_entity import UserEntity
from app.domain.interfaces.repositories.common_repository import ICommonRepository
from app.domain.interfaces.repositories.harvesting_repository import (
    IHarvestingRepository,
)
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class UpdateHarvestingReport(IUpdateHarvestingReportUC):
    def __init__(
        self,
        harvesting_repo: IHarvestingRepository,
        common_repo: ICommonRepository,
        query_helper: IQueryHelperService,
    ) -> None:
        self.harvesting_repo = harvesting_repo
        self.common_repo = common_repo
        self.query_helper = query_helper

    def execute(
        self,
        harvesting_dto,
        new_zone_level_ids,
        old_zone_level_ids,
        new_zone_id,
        old_zone_id,
    ):
        query_entity = self._create_harvesting_entity(harvesting_dto)

        harvesting_entity = self.harvesting_repo.get_harvesting_report_by_id(
            harvesting_entity=query_entity
        )

        if not harvesting_entity:
            raise BadRequestError("ETB_khong_tim_thay_bao_cao_harvesting")

        if query_entity.shift.id:
            self.query_helper.add_table(table_name="shifts", _id=query_entity.shift.id)

        if query_entity.factory.id:
            self.query_helper.add_table(
                table_name="factories", _id=query_entity.factory.id
            )

        join_sql = self.query_helper.join_ids_sql()

        if join_sql != "":
            ids_for_check = self.query_helper.all_params()

            result = self.common_repo.check_ids(sql=join_sql, ids=ids_for_check)

            self.query_helper.verify_ids(
                targets=[row[0] for row in result],
                sources=self.query_helper.all_tables(),
            )

        if query_entity.shift.id:
            harvesting_entity.change_shift(new_shift=query_entity.shift)

        if query_entity.factory.id:
            harvesting_entity.change_factory(new_factory=query_entity.factory)

        if query_entity.number_crates:
            harvesting_entity.change_number_crates(
                new_number_crates=query_entity.number_crates
            )

        if query_entity.number_crates_discarded:
            harvesting_entity.change_number_crates_discarded(
                new_number_crates_discarded=query_entity.number_crates_discarded
            )

        if query_entity.quantity_larvae:
            harvesting_entity.change_quantity_larvae(
                new_quantity_larvae=query_entity.quantity_larvae
            )

        if query_entity.notes:
            harvesting_entity.change_notes(new_notes=query_entity.notes)

        if query_entity.status:
            harvesting_entity.change_status(new_status=query_entity.status)

        logger.debug(f"harvesting_entity: {harvesting_entity}")

        self.harvesting_repo.update_harvesting_report(
            harvesting_entity=harvesting_entity,
            old_zone_level_ids=old_zone_level_ids,
            new_zone_level_ids=new_zone_level_ids,
            new_zone_id=new_zone_id,
            old_zone_id=old_zone_id,
        )

    def _create_harvesting_entity(self, harvesting_dto: HarvestingDTO):
        return HarvestingEntity(
            id=harvesting_dto.id,
            notes=harvesting_dto.notes,
            number_crates=harvesting_dto.number_crates,
            number_crates_discarded=harvesting_dto.number_crates_discarded,
            quantity_larvae=harvesting_dto.quantity_larvae,
            shift=ShiftEntity(id=harvesting_dto.shift.id),
            growing=None,
            factory=FactoryEntity(id=harvesting_dto.factory.id),
            status=FormStatusEnum.APPROVED.value,
        )
