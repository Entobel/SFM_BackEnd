from app.application.interfaces.use_cases.level.list_level_uc import IListLevelUC
from app.domain.entities.level_entity import LevelEntity
from app.domain.interfaces.repositories.level_repository import ILevelRepository


class ListLevelUC(IListLevelUC):
    def __init__(self, level_repo: ILevelRepository) -> None:
        self.level_repo = level_repo

    def execute(self, page: int, page_size: int, search: str, is_active: bool) -> dict[
                                                                                  "total": int,
                                                                                  "page": int,
                                                                                  "page_size": int,
                                                                                  "total_pages": int,
                                                                                  "items": list[LevelEntity]
                                                                                  ]:
        return self.level_repo.get_list_levels(page=page, page_size=page_size, search=search, is_active=is_active)
