from application.interfaces.use_cases.production_type.create_production_type_uc import \
    ICreateProductionTypeUC
from application.schemas.produciton_type_dto import ProductionTypeDTO
from core.exception import BadRequestError
from domain.entities.production_type_entity import ProductionTypeEntity
from domain.interfaces.repositories.production_type_repository import \
    IProductionTypeRepository


class CreateProductionTypeUC(ICreateProductionTypeUC):
    def __init__(self, repo: IProductionTypeRepository):
        self.repo = repo

    def execute(self, production_type_dto: ProductionTypeDTO) -> bool:

        if self.repo.get_production_type_by_name(production_type_dto.name):
            raise BadRequestError("ETB-loai_san_pham_da_ton_tai")

        production_entity = ProductionTypeEntity(
            name=production_type_dto.name,
            abbr_name=production_type_dto.abbr_name,
            description=production_type_dto.description,
        )

        is_success = self.repo.create_production_type(production_entity)

        if not is_success:
            raise BadRequestError("ETB-tao_loai_san_pham_that_bai")

        return True
