from app.application.dto.production_object_dto import ProductionObjectDTO
from app.application.interfaces.use_cases.production_object.update_production_object_uc import \
    IUpdateProductionObjectUC
from app.core.exception import BadRequestError
from app.domain.interfaces.repositories.production_object_repository import \
    IProductionObjectRepository


class UpdateProductionObjectUC(IUpdateProductionObjectUC):
    def __init__(self, repo: IProductionObjectRepository):
        self.repo = repo

    def execute(self, production_object_dto: ProductionObjectDTO) -> bool:
        production_object_entity = self.repo.get_production_object_by_id(
            id=production_object_dto.id
        )

        if production_object_entity is None:
            raise BadRequestError("ETB-production_object_not_found")

        if production_object_dto.name is not None:
            production_object_entity.change_name(name=production_object_dto.name)

        if production_object_dto.description is not None:
            production_object_entity.change_description(
                description=production_object_dto.description
            )

        is_success = self.repo.update_production_object(
            production_object_entity=production_object_entity
        )

        if not is_success:
            raise BadRequestError("ETB-cap_nhat_production_object_that_bai")

        return True
