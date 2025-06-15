from re import I, S
from loguru import logger
from app.application.interfaces.use_cases.growing.update_growing_report_uc import IUpdateGrowingReportUC
from app.core.constants.common_enums import FormStatusEnum
from app.core.exception import BadRequestError
from app.domain.entities.diet_entity import DietEntity
from app.domain.entities.factory_entity import FactoryEntity
from app.domain.entities.growing_entity import GrowingEntity
from app.domain.entities.production_object_entity import ProductionObjectEntity
from app.domain.entities.production_type_entity import ProductionTypeEntity
from app.domain.entities.shift_entity import ShiftEntity
from app.domain.entities.user_entity import UserEntity
from app.domain.interfaces.repositories.common_repository import ICommonRepository
from app.domain.interfaces.repositories.growing_repository import IGrowingRepository
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class UpdateGrowingReport(IUpdateGrowingReportUC):
    def __init__(
        self,
        growing_repo: IGrowingRepository,
        common_repo: ICommonRepository,
        query_helper: IQueryHelperService,
    ) -> None:
        self.growing_repo = growing_repo
        self.common_repo = common_repo
        self.query_helper = query_helper

    def execute(self, growing_dto, new_zone_level_ids, old_zone_level_ids, new_zone_id, old_zone_id):
        query_entity = GrowingEntity(
            id=growing_dto.id,
            notes=growing_dto.notes,
            number_crates=growing_dto.number_crates,
            substrate_moisture=growing_dto.substrate_moisture,
            diet=DietEntity(
                id=growing_dto.diet.id
            ),
            shift=ShiftEntity(
                id=growing_dto.shift.id
            ),
            factory=FactoryEntity(
                id=growing_dto.factory.id
            ),
            production_object=ProductionObjectEntity(
                id=growing_dto.production_object.id
            ),
            production_type=ProductionTypeEntity(
                id=growing_dto.production_type.id),
            approved_at=growing_dto.approved_at,
            approved_by=UserEntity(
                id=growing_dto.approved_by.id
            ),
            status=growing_dto.status
        )

        growing_entity = self.growing_repo.get_growing_report_by_id(
            growing_entity=query_entity)

        if not growing_entity:
            raise BadRequestError("ETB_khong_tim_thay_bao_cao_growing")

        if query_entity.status == FormStatusEnum.APPROVED.value:
            growing_entity.change_shift(new_shift=query_entity.shift)
            growing_entity.change_diet(new_diet=query_entity.diet)
            growing_entity.change_production_object(
                new_production_object=query_entity.production_object)
            growing_entity.change_production_type(
                new_production_type=query_entity.production_type)
            growing_entity.change_factory(new_factory=query_entity.factory)
            growing_entity.change_number_crates(
                new_number_crates=query_entity.number_crates)
            growing_entity.change_substrate_moisture(
                new_substrate_moisture=query_entity.substrate_moisture)
            growing_entity.change_notes(new_notes=query_entity.notes)
            growing_entity.change_status(new_status=query_entity.status)
            growing_entity.change_approved_at(
                new_approved_at=query_entity.approved_at)
            growing_entity.change_approved_by(
                new_approved_by=query_entity.approved_by)
            growing_entity.change_status(new_status=query_entity.status)
            growing_entity.change_rejected_at(new_rejected_at=None)
            growing_entity.change_rejected_by(new_rejected_by=None)
            growing_entity.change_rejected_reason(new_rejected_reason=None)

            self.growing_repo.update_growing_report(growing_entity=growing_entity, old_zone_level_ids=old_zone_level_ids,
                                                    new_zone_level_ids=new_zone_level_ids, new_zone_id=new_zone_id, old_zone_id=old_zone_id)
