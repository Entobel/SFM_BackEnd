from app.application.dto.production_object_dto import ProductionObjectDTO
from app.application.interfaces.use_cases.production_object.update_status_production_object_uc import \
    IUpdateStatusProductionObjectUC
from app.core.exception import BadRequestError
from app.domain.interfaces.repositories.production_object_repository import \
    IProductionObjectRepository


class UpdateStatusProductionObjectUC(IUpdateStatusProductionObjectUC):
    def __init__(self, repo: IProductionObjectRepository):
        self.repo = repo

    def execute(self, production_object_dto: ProductionObjectDTO) -> bool:
        production_object_entity = self.repo.get_production_object_by_id(
            id=production_object_dto.id
        )

        if production_object_entity is None:
            raise BadRequestError("ETB-production_object_not_found")

        if production_object_entity.is_active == production_object_dto.is_active:
            return True

        production_object_entity.change_is_active(
            is_active=production_object_dto.is_active
        )

        is_success = self.repo.update_status_production_object(
            production_object_entity=production_object_entity
        )

        if not is_success:
            raise BadRequestError("ETB-update_status_production_object_failed")

        return True
