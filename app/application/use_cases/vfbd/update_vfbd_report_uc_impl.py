from loguru import logger
from app.application.dto.vfbd_dto import VfbdDTO
from app.application.interfaces.use_cases.vfbd.update_vfbd_report_uc import (
    IUpdateVfbdReportUC,
)
from app.core.constants.common_enums import FormStatusEnum
from app.core.exception import BadRequestError
from app.domain.entities.dried_larvae_discharge_type_entity import (
    DriedLarvaeDischargeTypeEntity,
)
from app.domain.entities.dryer_product_type_entity import DryerProductTypeEntity
from app.domain.entities.factory_entity import FactoryEntity
from app.domain.entities.shift_entity import ShiftEntity
from app.domain.entities.user_entity import UserEntity
from app.domain.entities.vfbd_entity import VfbdEntity
from app.domain.interfaces.repositories.common_repository import ICommonRepository
from app.domain.interfaces.repositories.vfbd_repository import IVfbdRepository
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class UpdateVfbdReportUC(IUpdateVfbdReportUC):
    def __init__(
        self,
        vfbd_repository: IVfbdRepository,
        common_repository: ICommonRepository,
        query_helper: IQueryHelperService,
    ):
        self.vfbd_repository = vfbd_repository
        self.common_repository = common_repository
        self.query_helper = query_helper

    def execute(self, vfbd_dto: VfbdDTO) -> bool:
        query_entity = self._create_vfbd_entity(vfbd_dto=vfbd_dto)

        vfbd_entity = self.vfbd_repository.get_vfbd_report_by_id(
            vfbd_entity=query_entity
        )

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
        ids_for_check = self.query_helper.all_params()

        logger.debug(f"join_sql: {join_sql}")

        result = self.common_repository.check_ids(sql=join_sql, ids=ids_for_check)

        self.query_helper.verify_ids(
            targets=[row[0] for row in result], sources=self.query_helper.all_tables()
        )

        vfbd_entity.change_dried_larvae_discharge_type(
            dried_larvae_discharge_type=DriedLarvaeDischargeTypeEntity(
                id=query_entity.dried_larvae_discharge_type.id
            )
        )
        vfbd_entity.change_dryer_product_type(
            dryer_product_type=DryerProductTypeEntity(
                id=query_entity.dryer_product_type.id
            )
        )
        vfbd_entity.change_shift(shift=ShiftEntity(id=query_entity.shift.id))
        vfbd_entity.change_factory(factory=FactoryEntity(id=query_entity.factory.id))
        vfbd_entity.change_harvest_time(harvest_time=query_entity.harvest_time)
        vfbd_entity.change_temperature_output_1st(
            temperature_output_1st=query_entity.temperature_output_1st
        )
        vfbd_entity.change_temperature_output_2nd(
            temperature_output_2nd=query_entity.temperature_output_2nd
        )
        vfbd_entity.change_dried_larvae_moisture(
            dried_larvae_moisture=query_entity.dried_larvae_moisture
        )
        vfbd_entity.change_quantity_dried_larvae_sold(
            quantity_dried_larvae_sold=query_entity.quantity_dried_larvae_sold
        )
        vfbd_entity.change_drying_result(drying_result=query_entity.drying_result)
        vfbd_entity.change_notes(notes=query_entity.notes)
        vfbd_entity.change_status(status=query_entity.status)

        is_success = self.vfbd_repository.update_vfbd_report(vfbd_entity=vfbd_entity)

        if not is_success:
            raise BadRequestError("ETB_loi_khi_cap_nhat_vfbd_report")
        return True

    def _create_vfbd_entity(self, vfbd_dto: VfbdDTO) -> VfbdEntity:
        return VfbdEntity(
            date_reported=vfbd_dto.date_reported,
            shift=ShiftEntity(id=vfbd_dto.shift.id),
            factory=FactoryEntity(id=vfbd_dto.factory.id),
            start_time=vfbd_dto.start_time,
            end_time=vfbd_dto.end_time,
            dried_larvae_discharge_type=DriedLarvaeDischargeTypeEntity(
                id=vfbd_dto.dried_larvae_discharge_type.id
            ),
            harvest_time=vfbd_dto.harvest_time,
            temperature_output_1st=vfbd_dto.temperature_output_1st,
            temperature_output_2nd=vfbd_dto.temperature_output_2nd,
            dryer_product_type=DryerProductTypeEntity(
                id=vfbd_dto.dryer_product_type.id
            ),
            dried_larvae_moisture=vfbd_dto.dried_larvae_moisture,
            quantity_dried_larvae_sold=vfbd_dto.quantity_dried_larvae_sold,
            drying_result=vfbd_dto.drying_result,
            notes=vfbd_dto.notes,
            status=FormStatusEnum.PENDING.value,
        )
