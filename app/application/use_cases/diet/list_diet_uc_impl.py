from app.application.interfaces.use_cases.diet.list_diet_uc import IListDietUC
from app.domain.entities.diet_entity import DietEntity
from app.domain.interfaces.repositories.diet_repository import IDietRepository


class ListDietUC(IListDietUC):
    def __init__(self, diet_repository: IDietRepository):
        self.diet_repository = diet_repository

    def execute(
        self, page: int, page_size: int, search: str, is_active: bool = None
    ) -> dict[
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
        "items" : list[DietEntity],
    ]:
        return self.diet_repository.get_all_diets(
            page=page,
            page_size=page_size,
            search=search,
            is_active=is_active,
        )
