from app.application.interfaces.use_cases.vfbd.delete_vfbd_report_uc import (
    IDeleteVfbdReportUC,
)
from app.application.dto.vfbd_dto import VfbdDTO
from app.core.exception import BadRequestError
from app.domain.entities.vfbd_entity import VfbdEntity
from app.domain.interfaces.repositories.vfbd_repository import IVfbdRepository


class DeleteVfbdReportUC(IDeleteVfbdReportUC):
    def __init__(self, vfbd_repo: IVfbdRepository) -> None:
        self.vfbd_repo = vfbd_repo

    def execute(self, vfbd_dto: VfbdDTO):
        _vfbd_entity = self._create_vfbd_entity(vfbd_dto=vfbd_dto)

        vfbd_entity = self.vfbd_repo.get_vfbd_report_by_id(vfbd_entity=_vfbd_entity)

        if vfbd_entity is None:
            raise BadRequestError("ETB-vfbd_id_khong_ton_tai")

        vfbd_entity.change_is_active(new_is_active=False)

        is_success = self.vfbd_repo.delete_vfbd_report(vfbd_entity=vfbd_entity)

        if not is_success:
            return BadRequestError("Co_loi_khi_xoa_vfbd")

        return True

    def _create_vfbd_entity(self, vfbd_dto: VfbdDTO):
        return VfbdEntity(id=vfbd_dto.id)
