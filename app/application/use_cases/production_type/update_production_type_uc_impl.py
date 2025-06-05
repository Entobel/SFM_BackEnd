from app.application.dto.produciton_type_dto import ProductionTypeDTO
from app.application.interfaces.use_cases.production_type.update_production_type_uc import (
    IUpdateProductionTypeUC,
)
from app.core.exception import BadRequestError
from app.domain.entities.production_type_entity import ProductionTypeEntity
from app.domain.interfaces.repositories.production_type_repository import (
    IProductionTypeRepository,
)


class UpdateProductionTypeUC(IUpdateProductionTypeUC):
    def __init__(self, repo: IProductionTypeRepository):
        self.repo = repo

    def execute(self, production_type_dto: ProductionTypeDTO) -> bool:
        query_entity = ProductionTypeEntity(id=production_type_dto.id)

        production_type_entity = self.repo.get_production_type_by_id(
            production_type_entity=query_entity
        )

        if not production_type_entity:
            raise BadRequestError("ETB-loai_san_pham_khong_ton_tai")

        if (
            query_entity.name is not None
            and query_entity.name != production_type_entity.name
        ):
            if self.repo.get_production_type_by_name(query_entity.name):
                raise BadRequestError("ETB-ten_loai_san_pham_da_ton_tai")

            production_type_entity.change_name(query_entity.name)

        if (
            query_entity.abbr_name is not None
            and query_entity.abbr_name != production_type_entity.abbr_name
        ):
            production_type_entity.change_abbr_name(query_entity.abbr_name)

        if (
            query_entity.description is not None
            and query_entity.description != production_type_entity.description
        ):
            production_type_entity.change_description(query_entity.description)

        is_success = self.repo.update_production_type(production_type_entity)

        if not is_success:
            raise BadRequestError("ETB-cap_nhat_loai_san_pham_that_bai")

        return True
