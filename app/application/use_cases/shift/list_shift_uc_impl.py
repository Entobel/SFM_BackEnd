from app.application.interfaces.use_cases.shift.list_shift_uc import IListShiftUC
from app.domain.entities.shift_entity import ShiftEntity
from app.domain.interfaces.repositories.shift_repository import IShiftRepository


class ListShiftUC(IListShiftUC):
    def __init__(self, shift_repository: IShiftRepository):
        self.shift_repository = shift_repository

    def execute(
        self,
        page: int,
        page_size: int,
        search: str,
        is_active: bool,
    ) -> dict[
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
        "items" : list[ShiftEntity],
    ]:
        return self.shift_repository.get_all_shifts(page, page_size, search, is_active)
