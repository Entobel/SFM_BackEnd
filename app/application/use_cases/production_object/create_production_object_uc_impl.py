from application.interfaces.use_cases.production_object.create_production_object_uc import \
    ICreateProductionObjectUC
from application.schemas.production_object_schemas import ProductionObjectDTO
from core.exception import BadRequestError
from domain.entities.production_object_entity import ProductionObjectEntity
from domain.interfaces.repositories.production_object_repository import \
    IProductionObjectRepository


class CreateProductionObjectUC(ICreateProductionObjectUC):
    def __init__(self, production_object_repository: IProductionObjectRepository):
        self.production_object_repository = production_object_repository

    def execute(self, production_object_dto: ProductionObjectDTO) -> bool:
        is_exist = self.production_object_repository.get_production_object_by_name(
            name=production_object_dto.name
        )

        if is_exist:
            raise BadRequestError("ETB-production_object_da_ton_tai")

        production_object_entity = ProductionObjectEntity(
            name=production_object_dto.name,
            description=production_object_dto.description,
        )

        is_success = self.production_object_repository.create_production_object(
            production_object_entity=production_object_entity
        )

        if not is_success:
            raise BadRequestError("ETB-tao_production_object_that_bai")

        return True
