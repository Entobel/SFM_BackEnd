from application.interfaces.use_cases.diet.update_diet_uc import IUpdateDietUC
from application.schemas.diet_schemas import DietDTO
from core.exception import BadRequestError
from domain.interfaces.repositories.diet_repository import IDietRepository


class UpdateDietUC(IUpdateDietUC):
    def __init__(self, diet_repository: IDietRepository):
        self.diet_repository = diet_repository

    def execute(self, diet_dto: DietDTO) -> bool:
        diet_entity = self.diet_repository.get_diet_by_id(diet_dto.id)

        if diet_entity is None:
            raise BadRequestError("ETB-diet_khong_ton_tai")

        if diet_dto.name:
            diet_entity.change_name(diet_dto.name)

        if diet_dto.description:
            diet_entity.change_description(diet_dto.description)

        is_success = self.diet_repository.update_diet(diet_entity)

        if not is_success:
            raise BadRequestError("ETB-cap_nhat_diet_that_bai")

        return True
