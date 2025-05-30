from application.interfaces.use_cases.growing.create_growing_uc import \
    ICreateGrowingUC
from core.exception import BadRequestError
from domain.entities.diet_entity import DietEntity
from domain.entities.growing_entity import GrowingEntity
from domain.entities.production_object_entity import ProductionObjectEntity
from domain.entities.production_type_entity import ProductionTypeEntity
from domain.entities.shift_entity import ShiftEntity
from domain.entities.user_entity import UserEntity
from domain.interfaces.repositories.growing_repository import \
    IGrowingRepository
from presentation.schemas.growing_schema import CreateGrowingSchema


class CreateGrowingUC(ICreateGrowingUC):
    def __init__(self, growing_repository: IGrowingRepository):
        self.growing_repository = growing_repository

    def execute(self, body: CreateGrowingSchema):

        growing_entity = GrowingEntity(
            date_produced=body.date_produced,
            diet=DietEntity(id=body.diet_id),
            production_object=ProductionObjectEntity(id=body.production_object_id),
            production_type=ProductionTypeEntity(id=body.production_type_id),
            user=UserEntity(id=body.user_id),
            shift=ShiftEntity(id=body.shift_id),
            location_1=body.location_1,
            location_2=body.location_2,
            location_3=body.location_3,
            location_4=body.location_4,
            location_5=body.location_5,
            number_crates=body.number_crates,
            substrate_moisture=body.substrate_moisture,
            notes=body.notes,
        )

        is_success = self.growing_repository.create_new_growing(
            growing_entity=growing_entity
        )

        if not is_success:
            raise BadRequestError(error_code="ETB_khong_tao_duoc_growing")

        return True
