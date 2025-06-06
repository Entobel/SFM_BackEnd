from app.application.dto.produciton_type_dto import ProductionTypeDTO
from app.application.interfaces.use_cases.production_type.update_status_production_type_uc import (
    IUpdateStatusProductionTypeUC,
)
from app.core.exception import BadRequestError
from app.domain.entities.production_type_entity import ProductionTypeEntity
from app.domain.interfaces.repositories.production_type_repository import (
    IProductionTypeRepository,
)


class UpdateStatusProductionTypeUC(IUpdateStatusProductionTypeUC):
    def __init__(self, repo: IProductionTypeRepository):
        self.repo = repo

    def execute(self, production_type_dto: ProductionTypeDTO) -> bool:
        query_entity = ProductionTypeEntity(id=production_type_dto.id)

        production_type_entity = self.repo.get_production_type_by_id(
            production_type_entity=query_entity
        )

        if production_type_entity is None:
            raise BadRequestError("ETB-loai_san_pham_khong_ton_tai")

        if production_type_entity.is_active == query_entity.is_active:
            return True

        production_type_entity.change_is_active(is_active=production_type_dto.is_active)

        is_success = self.repo.update_status_production_type(
            production_type_entity=production_type_entity
        )

        if not is_success:
            raise BadRequestError("ETB-cap_nhat_trang_thai_loai_san_pham_that_bai")

        return True
