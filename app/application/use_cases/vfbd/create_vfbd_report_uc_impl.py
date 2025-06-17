from loguru import logger
from app.application.dto.vfbd_dto import VfbdDTO
from app.application.interfaces.use_cases.vfbd.create_vfbd_report_uc import ICreateVfbdReportUC
from app.core.constants.common_enums import FormStatusEnum
from app.core.exception import BadRequestError
from app.domain.entities.dried_larvae_discharge_type_entity import DriedLarvaeDischargeTypeEntity
from app.domain.entities.factory_entity import FactoryEntity
from app.domain.entities.product_type_entity import ProductTypeEntity
from app.domain.entities.shift_entity import ShiftEntity
from app.domain.entities.user_entity import UserEntity
from app.domain.entities.vfbd_entity import VfbdEntity
from app.domain.interfaces.repositories.common_repository import ICommonRepository
from app.domain.interfaces.repositories.vfbd_repository import IVfbdRepository
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class CreateVfbdReportUC(ICreateVfbdReportUC):
    def __init__(self, vfbd_repository: IVfbdRepository, common_repository: ICommonRepository, query_helper: IQueryHelperService):
        self.vfbd_repository = vfbd_repository
        self.common_repository = common_repository
        self.query_helper = query_helper

    def execute(self, vfbd_dto):
        if vfbd_dto.shift.id:
            self.query_helper.add_table(
                table_name="shifts", _id=vfbd_dto.shift.id
            )

        if vfbd_dto.factory.id:
            self.query_helper.add_table(
                table_name="factories", _id=vfbd_dto.factory.id
            )

        if vfbd_dto.dried_larvae_discharge_type.id:
            self.query_helper.add_table(
                table_name="dried_larvae_discharge_types", _id=vfbd_dto.dried_larvae_discharge_type.id)

        if vfbd_dto.product_type.id:
            self.query_helper.add_table(
                table_name="product_types", _id=vfbd_dto.product_type.id)

        if vfbd_dto.created_by.id:
            self.query_helper.add_table(
                table_name="users", _id=vfbd_dto.created_by.id)

        join_sql = self.query_helper.join_ids_sql()
        ids_for_check = self.query_helper.all_params()

        result = self.common_repository.check_ids(
            sql=join_sql, ids=ids_for_check)

        self.query_helper.verify_ids(
            targets=[row[0] for row in result], sources=self.query_helper.all_tables()
        )

        vfbd_entity = self._create_vfbd_entity(vfbd_dto=vfbd_dto)

        is_success = self.vfbd_repository.create_vfbd_report(
            vfbd_entity=vfbd_entity)

        if not is_success:
            raise BadRequestError("ETB_loi_khi_tao_vfbd_report")

        return True

    def _create_vfbd_entity(self, vfbd_dto: VfbdDTO) -> VfbdEntity:
        return VfbdEntity(
            date_reported=vfbd_dto.date_reported,
            shift=ShiftEntity(
                id=vfbd_dto.shift.id
            ),
            factory=FactoryEntity(
                id=vfbd_dto.factory.id
            ),
            start_time=vfbd_dto.start_time,
            end_time=vfbd_dto.end_time,
            dried_larvae_discharge_type=DriedLarvaeDischargeTypeEntity(
                id=vfbd_dto.dried_larvae_discharge_type.id),
            harvest_time=vfbd_dto.harvest_time,
            temperature_output_1st=vfbd_dto.temperature_output_1st,
            temperature_output_2nd=vfbd_dto.temperature_output_2nd,
            product_type=ProductTypeEntity(
                id=vfbd_dto.product_type.id
            ),
            dried_larvae_moisture=vfbd_dto.dried_larvae_moisture,
            quantity_dried_larvae_sold=vfbd_dto.quantity_dried_larvae_sold,
            drying_result=vfbd_dto.drying_result,
            notes=vfbd_dto.notes,
            created_by=UserEntity(
                id=vfbd_dto.created_by.id
            ),
            status=FormStatusEnum.PENDING.value
        )
