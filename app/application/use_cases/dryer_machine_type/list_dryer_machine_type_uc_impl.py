

from app.application.interfaces.use_cases.dryer_machine_type.list_dryer_machine_type_uc import IListDryerMachineTypeUC
from app.domain.interfaces.repositories.dryer_machine_type_repository import IDryerMachineTypeRepository


class ListDryerMachineTypeUC(IListDryerMachineTypeUC):
    def __init__(self, dryer_machine_repo: IDryerMachineTypeRepository):
        self.dryer_machine_repo = dryer_machine_repo

    def execute(self, page, page_size, search, is_active):
        return self.dryer_machine_repo.get_list_dryer_machine_types(
            page=page,
            page_size=page_size,
            search=search,
            is_active=is_active
        )
