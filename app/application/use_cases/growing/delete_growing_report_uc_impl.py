from app.application.dto.growing_dto import GrowingDTO


from app.application.interfaces.use_cases.growing.delete_growing_report_uc import (
    IDeleteGrowingReportUC,
)
from app.core.exception import BadRequestError
from app.domain.entities.growing_entity import GrowingEntity
from app.domain.interfaces.repositories.growing_repository import IGrowingRepository


class DeleteGrowingReportUC(IDeleteGrowingReportUC):
    def __init__(self, growing_repo: IGrowingRepository) -> None:
        self.growing_repo = growing_repo

    def execute(self, growing_dto: GrowingDTO):
        _growing_entity = self._create_growing_entity(growing_dto=growing_dto)
        # Check id is existed
        growing_entity = self.growing_repo.get_growing_report_by_id(
            growing_entity=_growing_entity
        )

        if growing_entity is None:
            raise BadRequestError("ETB-growing_id_khong_ton_tai")

        growing_entity.change_is_active(new_is_active=False)

        is_success = self.growing_repo.delete_growing(growing_entity=growing_entity)

        if not is_success:
            return BadRequestError("Co_loi_khi_xoa_growing")

        return True

    def _create_growing_entity(self, growing_dto: GrowingDTO):
        return GrowingEntity(id=growing_dto.id)
