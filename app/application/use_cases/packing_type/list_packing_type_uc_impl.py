from app.application.interfaces.use_cases.packing_type.list_packing_type_uc import IListPackingTypeUC
from app.domain.interfaces.repositories.packing_type_repository import IPackingTypeRepository


class ListPackingTypeUC(IListPackingTypeUC):
    def __init__(self, packing_repo: IPackingTypeRepository):
        self.packing_repo = packing_repo

    def execute(self, page, page_size, search, is_active):
        return self.packing_repo.get_list_packing_type(
            page=page,
            page_size=page_size,
            search=search,
            is_active=is_active
        )
