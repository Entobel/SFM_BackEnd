from domain.entities.growing_entity import GrowingEntity
from application.interfaces.use_cases.growing.list_growing_uc import IListGrowingUC

from domain.interfaces.repositories.growing_repository import IGrowingRepository


class ListGrowingUC(IListGrowingUC):
    def __init__(self, growing_repository: IGrowingRepository):
        self.growing_repository = growing_repository

    def execute(
        self,
        page: int,
        page_size: int,
        search: str | None,
        shift_id: int | None,
        production_type_id: int | None,
        production_object_id: int | None,
        diet_id: int | None,
        start_date: str | None,
        end_date: str | None,
    ) -> dict[
        "items" : list[GrowingEntity],
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
    ]:
        return self.growing_repository.get_all_growings(
            page=page,
            page_size=page_size,
            search=search,
            shift_id=shift_id,
            production_type_id=production_type_id,
            production_object_id=production_object_id,
            diet_id=diet_id,
            start_date=start_date,
            end_date=end_date,
        )
