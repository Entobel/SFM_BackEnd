from app.application.interfaces.use_cases.grinding.delete_grinding_report_uc import (
    IDeleteGrindingReportUC,
)
from app.application.dto.grinding_dto import GrindingDTO
from app.core.exception import BadRequestError
from app.domain.entities.grinding_entity import GrindingEntity
from app.domain.interfaces.repositories.grinding_repository import IGrindingRepository


class DeleteGrindingReportUC(IDeleteGrindingReportUC):
    def __init__(self, grinding_repo: IGrindingRepository) -> None:
        self.grinding_repo = grinding_repo

    def execute(self, grinding_dto: GrindingDTO):
        _grinding_entity = self._create_grinding_entity(grinding_dto=grinding_dto)

        grinding_entity = self.grinding_repo.get_grinding_by_id(
            grinding_entity=_grinding_entity
        )

        if grinding_entity is None:
            raise BadRequestError("ETB-grinding_id_khong_ton_tai")

        grinding_entity.change_is_active(new_is_active=False)

        is_success = self.grinding_repo.delete_grinding_report(
            grinding_entity=grinding_entity
        )

        if not is_success:
            return BadRequestError("Co_loi_khi_xoa_grinding")

        return True

    def _create_grinding_entity(self, grinding_dto: GrindingDTO):
        return GrindingEntity(id=grinding_dto.id)
