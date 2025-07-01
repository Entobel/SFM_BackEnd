from loguru import logger
from app.application.dto.dd_dto import DdDTO
from app.application.interfaces.use_cases.dd.update_dd_report_uc import (
    IUpdateDdReportUC,
)
from app.core.constants.common_enums import FormStatusEnum
from app.core.exception import BadRequestError
from app.domain.entities.dd_entity import DdEntity
from app.domain.entities.dried_larvae_discharge_type_entity import (
    DriedLarvaeDischargeTypeEntity,
)
from app.domain.entities.dryer_machine_type_entity import DryerMachineTypeEntity
from app.domain.entities.dryer_product_type_entity import DryerProductTypeEntity
from app.domain.entities.factory_entity import FactoryEntity
from app.domain.entities.shift_entity import ShiftEntity
from app.domain.interfaces.repositories.dd_repository import IDdRepository
from app.domain.interfaces.repositories.common_repository import ICommonRepository
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class UpdateDdReportUC(IUpdateDdReportUC):
    def __init__(
        self,
        dd_repository: IDdRepository,
        common_repository: ICommonRepository,
        query_helper: IQueryHelperService,
    ):
        self.dd_repository = dd_repository
        self.common_repository = common_repository
        self.query_helper = query_helper

    def execute(self, dd_dto: DdDTO) -> bool:
        query_entity = self._create_dd_entity(dd_dto=dd_dto)

        dd_entity = self.dd_repository.get_dd_report_by_id(dd_entity=query_entity)

        if dd_entity is None:
            raise BadRequestError("ETB_dd_report_khong_ton_tai")

        if query_entity.shift.id:
            self.query_helper.add_table(table_name="shifts", _id=query_entity.shift.id)

        if query_entity.factory.id:
            self.query_helper.add_table(
                table_name="factories", _id=query_entity.factory.id
            )

        if query_entity.dried_larvae_discharge_type.id:
            self.query_helper.add_table(
                table_name="dried_larvae_discharge_types",
                _id=query_entity.dried_larvae_discharge_type.id,
            )

        if query_entity.dryer_product_type.id:
            self.query_helper.add_table(
                table_name="dryer_product_types", _id=query_entity.dryer_product_type.id
            )

        join_sql = self.query_helper.join_ids_sql()

        if join_sql != "":

            ids_for_check = self.query_helper.all_params()

            result = self.common_repository.check_ids(sql=join_sql, ids=ids_for_check)

            self.query_helper.verify_ids(
                targets=[row[0] for row in result],
                sources=self.query_helper.all_tables(),
            )

        if query_entity.dryer_machine_type.id:
            dd_entity.change_dryer_machine_type(
                new_dryer_machine_type=DryerMachineTypeEntity(
                    id=query_entity.dryer_machine_type.id
                )
            )

        if query_entity.dried_larvae_discharge_type.id:
            dd_entity.change_dried_larvae_discharge_type(
                new_dried_larvae_discharge_type=DriedLarvaeDischargeTypeEntity(
                    id=query_entity.dried_larvae_discharge_type.id
                )
            )

        if query_entity.dryer_product_type.id:
            dd_entity.change_dryer_product_type(
                new_dryer_product_type=DryerProductTypeEntity(
                    id=query_entity.dryer_product_type.id
                )
            )

        if query_entity.shift.id:
            dd_entity.change_shift(new_shift=ShiftEntity(id=query_entity.shift.id))

        if query_entity.factory.id:
            dd_entity.change_factory(
                new_factory=FactoryEntity(id=query_entity.factory.id)
            )

        if query_entity.temperature_after_2h:
            dd_entity.change_temperature_after_2h(
                new_temperature=query_entity.temperature_after_2h
            )

        if query_entity.temperature_after_3h:
            dd_entity.change_temperature_after_3h(
                new_temperature=query_entity.temperature_after_3h
            )

        if query_entity.temperature_after_3h30:
            dd_entity.change_temperature_after_3h30(
                new_temperature=query_entity.temperature_after_3h30
            )

        if query_entity.temperature_after_4h:
            dd_entity.change_temperature_after_4h(
                new_temperature=query_entity.temperature_after_4h
            )

        if query_entity.temperature_after_4h30:
            dd_entity.change_temperature_after_4h30(
                new_temperature=query_entity.temperature_after_4h30
            )

        if query_entity.dried_larvae_moisture:
            dd_entity.change_dried_larvae_moisture(
                new_dried_larvae_moisture=query_entity.dried_larvae_moisture
            )

        if query_entity.quantity_dried_larvae_output:
            dd_entity.change_quantity_dried_larvae_output(
                new_quantity=query_entity.quantity_dried_larvae_output
            )

        if query_entity.quantity_fresh_larvae_input:
            dd_entity.change_quantity_fresh_larvae_input(
                new_quantity=query_entity.quantity_fresh_larvae_input
            )

        if query_entity.drying_result is not None:
            dd_entity.change_drying_result(new_drying_result=query_entity.drying_result)

        if query_entity.notes:
            dd_entity.change_notes(new_notes=query_entity.notes)

        if query_entity.status:
            dd_entity.change_status(new_status=query_entity.status)

        logger.debug(f"dd_entity: {dd_entity}")

        is_success = self.dd_repository.update_dd_report(dd_entity=dd_entity)

        if not is_success:
            raise BadRequestError("ETB_loi_khi_cap_nhat_dd_report")
        return True

    def _create_dd_entity(self, dd_dto: DdDTO) -> DdEntity:
        return DdEntity(
            id=dd_dto.id,
            shift=ShiftEntity(id=dd_dto.shift.id),
            factory=FactoryEntity(id=dd_dto.factory.id),
            dryer_machine_type=DryerMachineTypeEntity(id=dd_dto.dryer_machine_type.id),
            dried_larvae_discharge_type=DriedLarvaeDischargeTypeEntity(
                id=dd_dto.dried_larvae_discharge_type.id
            ),
            dryer_product_type=DryerProductTypeEntity(id=dd_dto.dryer_product_type.id),
            quantity_fresh_larvae_input=dd_dto.quantity_fresh_larvae_input,
            quantity_dried_larvae_output=dd_dto.quantity_dried_larvae_output,
            temperature_after_2h=dd_dto.temperature_after_2h,
            temperature_after_3h=dd_dto.temperature_after_3h,
            temperature_after_3h30=dd_dto.temperature_after_3h30,
            temperature_after_4h=dd_dto.temperature_after_4h,
            temperature_after_4h30=dd_dto.temperature_after_4h30,
            start_time=dd_dto.start_time,
            dried_larvae_moisture=dd_dto.dried_larvae_moisture,
            end_time=dd_dto.end_time,
            drying_result=dd_dto.drying_result,
            notes=dd_dto.notes,
            status=FormStatusEnum.APPROVED.value,
        )


# //  fat, ash, protein, fiber, moisture
