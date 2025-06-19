from app.application.interfaces.use_cases.dryer_product_type.list_dryer_product_type_uc import IListDryerProductTypeUC
from app.domain.interfaces.repositories.dryer_product_type_repository import IDryerProductTypeRepository


class ListDryerProductTypeUC(IListDryerProductTypeUC):
    def __init__(self, dryer_product_repo: IDryerProductTypeRepository):
        self.dryer_product_repo = dryer_product_repo

    def execute(self, page, page_size, search, is_active):
        return self.dryer_product_repo.get_list_dryer_product_types(
            page=page,
            page_size=page_size,
            search=search,
            is_active=is_active
        )
