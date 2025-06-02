from app.application.dto.level_dto import LevelDTO
from app.application.interfaces.use_cases.level.create_level_uc import ICreateLevelUC
from app.core.exception import BadRequestError
from app.domain.entities.level_entity import LevelEntity
from app.domain.interfaces.repositories.level_repository import ILevelRepository


class CreateLevelUC(ICreateLevelUC):
    def __init__(self, level_repo: ILevelRepository):
        self.level_repo = level_repo

    def execute(self, level_dto: LevelDTO) -> bool:
        level_entity = LevelEntity(
            name=level_dto.name,
        )

        is_existed = self.level_repo.get_level_by_name(level_entity=level_entity)

        if is_existed:
            raise BadRequestError("ETB_da_ton_tai_level")

        is_success = self.level_repo.create_level(level_entity=level_entity)

        if not is_success:
            raise BadRequestError("ETB_tao_level_khong_thanh_cong")

        return True
