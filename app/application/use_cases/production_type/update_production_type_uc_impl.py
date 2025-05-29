from application.interfaces.use_cases.production_type.update_production_type_uc import (
    IUpdateProductionTypeUC,
)
from application.schemas.produciton_type_dto import ProductionTypeDTO
from core.exception import BadRequestError
from domain.interfaces.repositories.production_type_repository import (
    IProductionTypeRepository,
)


class UpdateProductionTypeUC(IUpdateProductionTypeUC):
    def __init__(self, repo: IProductionTypeRepository):
        self.repo = repo

    def execute(self, production_type_dto: ProductionTypeDTO) -> bool:
        production_type_entity = self.repo.get_production_type_by_id(
            production_type_dto.id
        )
        if not production_type_entity:
            raise BadRequestError("ETB-loai_san_pham_khong_ton_tai")

        if (
            production_type_dto.name is not None
            and production_type_dto.name != production_type_entity.name
        ):
            if self.repo.get_production_type_by_name(production_type_dto.name):
                raise BadRequestError("ETB-ten_loai_san_pham_da_ton_tai")

            production_type_entity.change_name(production_type_dto.name)

        if (
            production_type_dto.abbr_name is not None
            and production_type_dto.abbr_name != production_type_entity.abbr_name
        ):
            production_type_entity.change_abbr_name(production_type_dto.abbr_name)

        if (
            production_type_dto.description is not None
            and production_type_dto.description != production_type_entity.description
        ):
            production_type_entity.change_description(production_type_dto.description)

        is_success = self.repo.update_production_type(production_type_entity)

        if not is_success:
            raise BadRequestError("ETB-cap_nhat_loai_san_pham_that_bai")

        return True
