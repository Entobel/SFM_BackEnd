from application.interfaces.use_cases.diet.update_status_diet_uc import \
    IUpdateStatusDietUC
from application.schemas.diet_schemas import DietDTO
from core.exception import BadRequestError
from domain.entities.diet_entity import DietEntity
from domain.interfaces.repositories.diet_repository import IDietRepository


class UpdateStatusDietUC(IUpdateStatusDietUC):
    def __init__(self, diet_repository: IDietRepository):
        self.diet_repository = diet_repository

    def execute(self, diet_dto: DietDTO) -> bool:
        diet_entity = self.diet_repository.get_diet_by_id(diet_dto.id)

        if not diet_entity:
            raise BadRequestError("ETB-diet_khong_ton_tai")

        if diet_entity.is_active == diet_dto.is_active:
            return True

        diet_entity.change_status(diet_dto.is_active)

        return self.diet_repository.update_diet_status(diet_entity=diet_entity)
