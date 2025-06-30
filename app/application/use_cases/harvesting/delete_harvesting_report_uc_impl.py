from app.application.interfaces.use_cases.harvesting.delete_harvesting_report_uc import (
    IDeleteHarvestingReportUC,
)
from app.application.dto.harvesting_dto import HarvestingDTO
from app.core.exception import BadRequestError
from app.domain.entities.harvesting_entity import HarvestingEntity
from app.domain.interfaces.repositories.harvesting_repository import (
    IHarvestingRepository,
)


class DeleteHarvestingReportUC(IDeleteHarvestingReportUC):
    def __init__(self, harvesting_repo: IHarvestingRepository) -> None:
        self.harvesting_repo = harvesting_repo

    def execute(self, harvesting_dto: HarvestingDTO):
        _harvesting_entity = self._create_harvesting_entity(
            harvesting_dto=harvesting_dto
        )

        harvesting_entity = self.harvesting_repo.get_harvesting_report_by_id(
            harvesting_entity=_harvesting_entity
        )

        if harvesting_entity is None:
            raise BadRequestError("ETB-harvesting_id_khong_ton_tai")

        harvesting_entity.change_is_active(new_is_active=False)

        is_success = self.harvesting_repo.delete_harvesting(
            harvesting_entity=harvesting_entity
        )

        if not is_success:
            return BadRequestError("Co_loi_khi_xoa_harvesting")

        return True

    def _create_harvesting_entity(self, harvesting_dto: HarvestingDTO):
        return HarvestingEntity(id=harvesting_dto.id)
