from app.application.dto.level_dto import LevelDTO
from app.application.interfaces.use_cases.level.update_status_level_uc import IUpdateStatusLevelUC
from app.core.exception import BadRequestError
from app.domain.entities.level_entity import LevelEntity
from app.domain.interfaces.repositories.level_repository import ILevelRepository


class UpdateStatusLevelUC(IUpdateStatusLevelUC):
    def __init__(self, level_repo: ILevelRepository):
        self.level_repo = level_repo

    def execute(self, level_dto: LevelDTO) -> bool:
        query_entity = LevelEntity(
            id=level_dto.id,
            is_active=level_dto.is_active,
        )

        # check exist
        level_entity = self.level_repo.get_level_by_id(level_entity=query_entity)

        if not level_entity:
            raise BadRequestError("ETB_level_khong_ton_tai")

        if level_entity.is_active == query_entity.is_active:
            return True

        level_entity.change_status(new_is_active=query_entity.is_active)

        is_success = self.level_repo.update_status_level(level_entity=level_entity)

        if not is_success:
            raise BadRequestError("ETB_cap_nhat_level_khong_thanh_cong")

        return True
