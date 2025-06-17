from app.application.dto.product_type_dto import ProductTypeDTO
from app.application.interfaces.use_cases.product_type.create_product_type_uc import \
    ICreateProductTypeUC
from app.core.exception import BadRequestError
from app.domain.entities.product_type_entity import ProductTypeEntity
from app.domain.interfaces.repositories.product_type_repository import \
    IProductTypeRepository


class CreateProductTypeUC(ICreateProductTypeUC):
    def __init__(self, product_type_repository: IProductTypeRepository):
        self.product_type_repository = product_type_repository

    def execute(self, product_type_dto: ProductTypeDTO) -> bool:
        is_exist = self.product_type_repository.get_product_type_by_name(
            name=product_type_dto.name
        )

        if is_exist:
            raise BadRequestError("ETB-product_type_da_ton_tai")

        product_type_entity = ProductTypeEntity(
            name=product_type_dto.name,
            description=product_type_dto.description,
        )

        is_success = self.product_type_repository.create_product_type(
            product_type_entity=product_type_entity
        )

        if not is_success:
            raise BadRequestError("ETB-tao_product_type_that_bai")

        return True
