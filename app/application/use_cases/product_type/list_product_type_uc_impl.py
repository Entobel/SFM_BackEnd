from app.application.interfaces.use_cases.product_type.list_product_type_uc import \
    IListProductTypeUC
from app.domain.entities.product_type_entity import ProductTypeEntity
from app.domain.interfaces.repositories.product_type_repository import \
    IProductTypeRepository


class ListProductTypeUC(IListProductTypeUC):
    def __init__(self, repo: IProductTypeRepository):
        self.repo = repo

    def execute(
        self, page: int, page_size: int, search: str, is_active: bool
    ) -> dict[
        "total":int,
        "page":int,
        "page_size":int,
        "total_pages":int,
        "items": list[ProductTypeEntity],
    ]:
        return self.repo.get_all_product_types(page, page_size, search, is_active)
