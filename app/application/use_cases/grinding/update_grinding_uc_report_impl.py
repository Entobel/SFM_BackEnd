from app.application.dto.grinding_dto import GrindingDTO
from app.application.interfaces.use_cases.grinding.update_grinding_report_uc import (
    IUpdateGrindingReportUC,
)
from app.core.constants.common_enums import FormStatusEnum
from app.core.exception import BadRequestError
from app.domain.entities.antioxidiant_type_entity import AntioxidantTypeEntity
from app.domain.entities.factory_entity import FactoryEntity
from app.domain.entities.grinding_entity import GrindingEntity
from app.domain.entities.packing_type_entity import PackingTypeEntity
from app.domain.entities.shift_entity import ShiftEntity
from app.domain.interfaces.repositories.common_repository import ICommonRepository
from app.domain.interfaces.repositories.grinding_repository import IGrindingRepository
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class UpdateGrindingReportUC(IUpdateGrindingReportUC):
    def __init__(
        self,
        grinding_repo: IGrindingRepository,
        common_repo: ICommonRepository,
        query_helper: IQueryHelperService,
    ):
        self.grinding_repo = grinding_repo
        self.common_repo = common_repo
        self.query_helper = query_helper

    def execute(self, grinding_dto: GrindingDTO) -> bool:
        query_entity = self._create_grinding_entity(grinding_dto=grinding_dto)

        grinding_entity = self.grinding_repo.get_grinding_by_id(
            grinding_entity=query_entity
        )

        if grinding_entity is None:
            raise BadRequestError("ETB_grinding_report_khong_ton_tai")

        if query_entity.shift.id:
            self.query_helper.add_table(table_name="shifts", _id=query_entity.shift.id)

        if query_entity.factory.id:
            self.query_helper.add_table(
                table_name="factories", _id=query_entity.factory.id
            )

        if query_entity.packing_type.id:
            self.query_helper.add_table(
                table_name="packing_types", _id=query_entity.packing_type.id
            )

        if query_entity.antioxidant_type.id:
            self.query_helper.add_table(
                table_name="antioxidant_types", _id=query_entity.antioxidant_type.id
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
            grinding_entity.change_shift(
                new_shift=ShiftEntity(id=query_entity.shift.id)
            )

        if query_entity.factory.id:
            grinding_entity.change_factory(
                new_factory=FactoryEntity(id=query_entity.factory.id)
            )

        if query_entity.start_time:
            grinding_entity.change_start_time(new_start_time=query_entity.start_time)

        if query_entity.end_time:
            grinding_entity.change_end_time(new_end_time=query_entity.end_time)

        if query_entity.packing_type.id:
            grinding_entity.change_packing_type(
                new_packing_type=PackingTypeEntity(id=query_entity.packing_type.id)
            )

        if query_entity.antioxidant_type.id:
            grinding_entity.change_antioxidant_type(
                new_antioxidant_type=AntioxidantTypeEntity(
                    id=query_entity.antioxidant_type.id
                )
            )

        if query_entity.batch_grinding_information:
            grinding_entity.change_batch_grinding_information(
                new_batch_grinding_information=query_entity.batch_grinding_information
            )

        if query_entity.quantity:
            grinding_entity.change_quantity(new_quantity=query_entity.quantity)

        if query_entity.notes:
            grinding_entity.change_notes(new_notes=query_entity.notes)

        if query_entity.status:
            grinding_entity.change_status(new_status=query_entity.status)

        is_success = self.grinding_repo.update_grinding(grinding_entity=grinding_entity)

        if not is_success:
            raise BadRequestError("ETB_loi_khi_cap_nhat_grinding_report")
        return True

    def _create_grinding_entity(self, grinding_dto: GrindingDTO) -> GrindingEntity:
        return GrindingEntity(
            id=grinding_dto.id,
            date_reported=grinding_dto.date_reported,
            quantity=grinding_dto.quantity,
            start_time=grinding_dto.start_time,
            end_time=grinding_dto.end_time,
            batch_grinding_information=grinding_dto.batch_grinding_information,
            shift=ShiftEntity(id=grinding_dto.shift.id),
            factory=FactoryEntity(id=grinding_dto.factory.id),
            antioxidant_type=AntioxidantTypeEntity(id=grinding_dto.antioxidant_type.id),
            packing_type=PackingTypeEntity(id=grinding_dto.packing_type.id),
            notes=grinding_dto.notes,
            status=FormStatusEnum.APPROVED.value,
        )
