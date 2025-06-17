from app.application.dto.product_type_dto import ProductTypeDTO
from app.application.interfaces.use_cases.product_type.update_product_type_uc import (
    IUpdateProductTypeUC,
)
from app.core.exception import BadRequestError
from app.domain.entities.product_type_entity import ProductTypeEntity
from app.domain.interfaces.repositories.product_type_repository import (
    IProductTypeRepository,
)


class UpdateProductTypeUC(IUpdateProductTypeUC):
    def __init__(self, repo: IProductTypeRepository):
        self.repo = repo

    def execute(self, product_type_dto: ProductTypeDTO) -> bool:
        query_entity = ProductTypeEntity(id=product_type_dto.id)

        product_type_entity = self.repo.get_product_type_by_id(
            product_type_entity=query_entity
        )

        if product_type_entity is None:
            raise BadRequestError("ETB-product_type_not_found")

        if product_type_dto.name is not None:
            product_type_entity.change_name(
                name=product_type_dto.name)

        if product_type_dto.description is not None:
            product_type_entity.change_description(
                description=product_type_dto.description
            )

        is_success = self.repo.update_product_type(
            product_type_entity=product_type_entity
        )

        if not is_success:
            raise BadRequestError("ETB-cap_nhat_product_type_that_bai")

        return True
