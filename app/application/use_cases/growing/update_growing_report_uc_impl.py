from re import I, S
from loguru import logger
from app.application.interfaces.use_cases.growing.update_growing_report_uc import (
    IUpdateGrowingReportUC,
)
from app.core.constants.common_enums import FormStatusEnum
from app.core.exception import BadRequestError
from app.domain.entities.diet_entity import DietEntity
from app.domain.entities.factory_entity import FactoryEntity
from app.domain.entities.growing_entity import GrowingEntity
from app.domain.entities.product_type_entity import ProductTypeEntity
from app.domain.entities.operation_type_entity import OperationTypeEntity
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

    def execute(
        self,
        growing_dto,
        new_zone_level_ids,
        old_zone_level_ids,
        new_zone_id,
        old_zone_id,
    ):
        query_entity = GrowingEntity(
            id=growing_dto.id,
            notes=growing_dto.notes,
            number_crates=growing_dto.number_crates,
            substrate_moisture=growing_dto.substrate_moisture,
            diet=DietEntity(id=growing_dto.diet.id),
            shift=ShiftEntity(id=growing_dto.shift.id),
            factory=FactoryEntity(id=growing_dto.factory.id),
            product_type=ProductTypeEntity(id=growing_dto.product_type.id),
            operation_type=OperationTypeEntity(id=growing_dto.operation_type.id),
            approved_at=growing_dto.approved_at,
            approved_by=UserEntity(id=growing_dto.approved_by.id),
            status=growing_dto.status,
        )

        growing_entity = self.growing_repo.get_growing_report_by_id(
            growing_entity=query_entity
        )

        if growing_entity is None:
            raise BadRequestError("ETB_khong_tim_thay_bao_cao_growing")

        if query_entity.shift.id:
            self.query_helper.add_table(table_name="shifts", _id=query_entity.shift.id)

        if query_entity.factory.id:
            self.query_helper.add_table(
                table_name="factories", _id=query_entity.factory.id
            )

        if query_entity.diet.id:
            self.query_helper.add_table(table_name="diets", _id=query_entity.diet.id)

        if query_entity.product_type.id:
            self.query_helper.add_table(
                table_name="product_types", _id=query_entity.product_type.id
            )

        if query_entity.operation_type.id:
            self.query_helper.add_table(
                table_name="operation_types", _id=query_entity.operation_type.id
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
            growing_entity.change_shift(new_shift=query_entity.shift)

        if query_entity.factory.id:
            growing_entity.change_factory(new_factory=query_entity.factory)

        if query_entity.diet.id:
            growing_entity.change_diet(new_diet=query_entity.diet)

        if query_entity.product_type.id:
            growing_entity.change_product_type(
                new_product_type=query_entity.product_type
            )

        if query_entity.operation_type.id:
            growing_entity.change_operation_type(
                new_operation_type=query_entity.operation_type
            )

        if query_entity.number_crates:
            growing_entity.change_number_crates(
                new_number_crates=query_entity.number_crates
            )

        if query_entity.substrate_moisture:
            growing_entity.change_substrate_moisture(
                new_substrate_moisture=query_entity.substrate_moisture
            )

        if query_entity.notes:
            growing_entity.change_notes(new_notes=query_entity.notes)

        if query_entity.status:
            growing_entity.change_status(new_status=query_entity.status)

        if query_entity.status:
            growing_entity.change_status(new_status=query_entity.status)

        self.growing_repo.update_growing_report(
            growing_entity=growing_entity,
            old_zone_level_ids=old_zone_level_ids,
            new_zone_level_ids=new_zone_level_ids,
            new_zone_id=new_zone_id,
            old_zone_id=old_zone_id,
        )
