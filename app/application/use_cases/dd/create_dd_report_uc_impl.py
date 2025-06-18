from loguru import logger
from app.application.dto.dd_dto import DdDTO
from app.application.interfaces.use_cases.dd.create_dd_report_uc import ICreateDdReportUC
from app.core.constants.common_enums import FormStatusEnum
from app.core.exception import BadRequestError
from app.domain.entities.dd_entity import DdEntity
from app.domain.entities.dried_larvae_discharge_type_entity import DriedLarvaeDischargeTypeEntity
from app.domain.entities.dryer_machine_type_entity import DryerMachineTypeEntity
from app.domain.entities.dryer_product_type_entity import DryerProductTypeEntity
from app.domain.entities.factory_entity import FactoryEntity
from app.domain.entities.shift_entity import ShiftEntity
from app.domain.entities.user_entity import UserEntity
from app.domain.interfaces.repositories.common_repository import ICommonRepository
from app.domain.interfaces.repositories.dd_repository import IDdRepository
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class CreateDDReportUC(ICreateDdReportUC):
    def __init__(self, dd_repository: IDdRepository, common_repository: ICommonRepository, query_helper: IQueryHelperService):
        self.dd_repository = dd_repository
        self.common_repository = common_repository
        self.query_helper = query_helper

    def execute(self, dd_dto):
        if dd_dto.shift.id:
            self.query_helper.add_table(
                table_name="shifts", _id=dd_dto.shift.id
            )

        if dd_dto.factory.id:
            self.query_helper.add_table(
                table_name="factories", _id=dd_dto.factory.id
            )

        if dd_dto.dried_larvae_discharge_type.id:
            self.query_helper.add_table(
                table_name="dried_larvae_discharge_types", _id=dd_dto.dried_larvae_discharge_type.id
            )

        if dd_dto.dryer_machine_type.id:
            self.query_helper.add_table(
                table_name="dryer_machine_types", _id=dd_dto.dryer_machine_type.id
            )

        if dd_dto.dryer_product_type.id:
            self.query_helper.add_table(
                table_name="dryer_product_types", _id=dd_dto.dryer_product_type.id
            )

        if dd_dto.created_by.id:
            self.query_helper.add_table(
                table_name="users", _id=dd_dto.created_by.id)

        join_sql = self.query_helper.join_ids_sql()
        ids_for_check = self.query_helper.all_params()

        result = self.common_repository.check_ids(
            sql=join_sql, ids=ids_for_check)

        self.query_helper.verify_ids(
            targets=[row[0] for row in result], sources=self.query_helper.all_tables()
        )

        dd_entity = self._create_dd_entity(dd_dto=dd_dto)

        is_success = self.dd_repository.create_dd_report(dd_entity=dd_entity)

        if not is_success:
            raise BadRequestError("ETB_loi_khi_tao_dd_report")

        return True

    def _create_dd_entity(self, dd_dto: DdDTO) -> DdEntity:
        return DdEntity(
            date_reported=dd_dto.date_reported,
            shift=ShiftEntity(id=dd_dto.shift.id),
            factory=FactoryEntity(id=dd_dto.factory.id),
            dryer_machine_type=DryerMachineTypeEntity(
                id=dd_dto.dryer_machine_type.id
            ),
            dryer_product_type=DryerProductTypeEntity(
                id=dd_dto.dryer_product_type.id
            ),
            dried_larvae_discharge_type=DriedLarvaeDischargeTypeEntity(
                id=dd_dto.dried_larvae_discharge_type.id
            ),
            quantity_fresh_larvae_input=dd_dto.quantity_fresh_larvae_input,
            quantity_dried_larvae_output=dd_dto.quantity_dried_larvae_output,
            temperature_after_2h=dd_dto.temperature_after_2h,
            temperature_after_3h=dd_dto.temperature_after_3h,
            temperature_after_3h30=dd_dto.temperature_after_3h30,
            temperature_after_4h=dd_dto.temperature_after_4h,
            temperature_after_4h30=dd_dto.temperature_after_4h30,
            dried_larvae_moisture=dd_dto.dried_larvae_moisture,
            start_time=dd_dto.start_time,
            end_time=dd_dto.end_time,
            drying_results=dd_dto.drying_results,
            notes=dd_dto.notes,
            created_by=UserEntity(
                id=dd_dto.created_by.id) if dd_dto.created_by else None,
            status=FormStatusEnum.APPROVED.value
        )
