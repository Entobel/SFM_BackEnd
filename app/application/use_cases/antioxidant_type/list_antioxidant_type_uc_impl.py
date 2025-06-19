from app.application.interfaces.use_cases.antioxidant_type.list_antioxidant_type_uc import IListAntioxidantTypeUC
from app.domain.interfaces.repositories.antioxidant_type_repository import IAntioxidantTypeRepository


class ListAntioxidantTypeUC(IListAntioxidantTypeUC):
    def __init__(self, antioxidant_repo: IAntioxidantTypeRepository):
        self.antioxidant_repo = antioxidant_repo

    def execute(self, page, page_size, search, is_active):
        return self.antioxidant_repo.get_list_antioxidant_types(
            page=page,
            page_size=page_size,
            search=search,
            is_active=is_active
        )
