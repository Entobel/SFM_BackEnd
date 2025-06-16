from app.application.dto.grinding_dto import GrindingDTO
from app.application.interfaces.use_cases.grinding.create_grinding_uc import ICreateGrindingUC
from app.core.constants.common_enums import FormStatusEnum
from app.core.exception import BadRequestError
from app.domain.entities.antioxidiant_type_entity import AntioxidantTypeEntity
from app.domain.entities.factory_entity import FactoryEntity
from app.domain.entities.grinding_entity import GrindingEntity
from app.domain.entities.packing_type_entity import PackingTypeEntity
from app.domain.entities.shift_entity import ShiftEntity
from app.domain.entities.user_entity import UserEntity
from app.domain.interfaces.repositories.common_repository import ICommonRepository
from app.domain.interfaces.repositories.grinding_repository import IGrindingRepository
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class CreateGrindingUC(ICreateGrindingUC):
    def __init__(
        self,
        grinding_repo: IGrindingRepository,
        query_helper: IQueryHelperService,
        common_repo: ICommonRepository,
    ) -> None:
        self.grinding_repo = grinding_repo
        self.query_helper = query_helper
        self.common_repo = common_repo

    def execute(self, grinding_dto):
        grinding_entity = self._create_grinding_entity(
            grinding_dto=grinding_dto)

        if grinding_entity.shift.id:
            self.query_helper.add_table(
                table_name="shifts", _id=grinding_entity.shift.id)

        if grinding_entity.packing_type.id:
            self.query_helper.add_table(
                table_name="packing_types", _id=grinding_entity.packing_type.id)

        if grinding_entity.antioxidant_type.id:
            self.query_helper.add_table(
                table_name="antioxidant_types", _id=grinding_entity.antioxidant_type.id)

        join_sql = self.query_helper.join_ids_sql()
        ids_for_check = self.query_helper.all_params()

        result = self.common_repo.check_ids(sql=join_sql, ids=ids_for_check)

        self.query_helper.verify_ids(
            targets=[row[0] for row in result], sources=self.query_helper.all_tables()
        )

        is_success = self.grinding_repo.create_grinding(
            grinding_entity=grinding_entity)

        if not is_success:
            raise BadRequestError("ETB_loi_khi_tao_grinding_report")

        return True

    def _create_grinding_entity(self, grinding_dto: GrindingDTO) -> GrindingEntity:
        """Create a Grinding from DTO with proper entity mapping."""

        return GrindingEntity(
            date_reported=grinding_dto.date_reported,
            quantity=grinding_dto.quantity,
            batch_grinding_information=grinding_dto.batch_grinding_information,
            shift=ShiftEntity(id=grinding_dto.shift.id),
            factory=FactoryEntity(id=grinding_dto.factory.id),
            antioxidant_type=AntioxidantTypeEntity(
                id=grinding_dto.antioxidant_type.id),
            packing_type=PackingTypeEntity(id=grinding_dto.packing_type.id),
            created_by=UserEntity(id=grinding_dto.user.id),
            notes=grinding_dto.notes,
            status=FormStatusEnum.PENDING.value
        )
