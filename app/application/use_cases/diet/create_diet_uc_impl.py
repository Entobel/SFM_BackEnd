from application.dto.diet_dto import DietDTO
from application.interfaces.use_cases.diet.create_diet_uc import ICreateDietUC
from core.exception import BadRequestError
from domain.entities.diet_entity import DietEntity
from domain.interfaces.repositories.diet_repository import IDietRepository


class CreateDietUC(ICreateDietUC):
    def __init__(self, diet_repository: IDietRepository):
        self.diet_repository = diet_repository

    def execute(self, diet_dto: DietDTO) -> bool:
        is_exist = self.diet_repository.get_diet_by_name(diet_dto.name)

        if is_exist:
            raise BadRequestError("ETB-diet_da_ton_tai")

        diet_entity = DietEntity(name=diet_dto.name, description=diet_dto.description)

        is_success = self.diet_repository.create_new_diet(diet_entity)

        if not is_success:
            raise BadRequestError("ETB-tao_di_that_bai")

        return True
