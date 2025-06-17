from app.application.dto.product_type_dto import ProductTypeDTO
from app.application.interfaces.use_cases.product_type.update_status_product_type_uc import (
    IUpdateStatusProductTypeUC,
)
from app.core.exception import BadRequestError
from app.domain.entities.product_type_entity import ProductTypeEntity
from app.domain.interfaces.repositories.product_type_repository import (
    IProductTypeRepository,
)


class UpdateStatusProductTypeUC(IUpdateStatusProductTypeUC):
    def __init__(self, repo: IProductTypeRepository):
        self.repo = repo

    def execute(self, product_type_dto: ProductTypeDTO) -> bool:
        query_entity = ProductTypeEntity(id=product_type_dto.id)

        product_type_entity = self.repo.get_product_type_by_id(
            product_type_entity=query_entity
        )

        if product_type_entity is None:
            raise BadRequestError("ETB-product_type_not_found")

        if product_type_entity.is_active == query_entity.is_active:
            return True

        product_type_entity.change_is_active(
            is_active=product_type_dto.is_active
        )

        is_success = self.repo.update_status_product_type(
            product_type_entity=product_type_entity
        )

        if not is_success:
            raise BadRequestError("ETB-update_status_product_type_failed")

        return True
