from app.application.interfaces.use_cases.dd.delete_dd_report_uc import (
    IDeleteDdReportUC,
)
from app.application.dto.dd_dto import DdDTO
from app.core.exception import BadRequestError
from app.domain.entities.dd_entity import DdEntity
from app.domain.interfaces.repositories.dd_repository import IDdRepository


class DeleteDdReportUC(IDeleteDdReportUC):
    def __init__(self, dd_repo: IDdRepository) -> None:
        self.dd_repo = dd_repo

    def execute(self, dd_dto: DdDTO):
        _dd_entity = self._create_dd_entity(dd_dto=dd_dto)

        dd_entity = self.dd_repo.get_dd_report_by_id(dd_entity=_dd_entity)

        if dd_entity is None:
            raise BadRequestError("ETB-dd_id_khong_ton_tai")

        dd_entity.change_is_active(new_is_active=False)

        is_success = self.dd_repo.delete_dd_report(dd_entity=dd_entity)

        if not is_success:
            return BadRequestError("Co_loi_khi_xoa_dd")

        return True

    def _create_dd_entity(self, dd_dto: DdDTO):
        return DdEntity(id=dd_dto.id)
