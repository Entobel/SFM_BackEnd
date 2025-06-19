

from app.application.interfaces.use_cases.dried_larvae_discharge_type.list_dried_larvae_discharge_type_uc import IListDriedLarvaeDischargeTypeUC
from app.application.interfaces.use_cases.dryer_machine_type.list_dryer_machine_type_uc import IListDryerMachineTypeUC
from app.domain.interfaces.repositories.dried_larvae_discharge_type_repository import IDriedLarvaeDischargeTypeRepository
from app.domain.interfaces.repositories.dryer_machine_type_repository import IDryerMachineTypeRepository


class ListDriedLarvaeDischargeTypeUC(IListDriedLarvaeDischargeTypeUC):
    def __init__(self, dried_larvae_discharge_type_repo: IDriedLarvaeDischargeTypeRepository):
        self.dried_larvae_discharge_type_repo = dried_larvae_discharge_type_repo

    def execute(self, page, page_size, search, is_active):
        return self.dried_larvae_discharge_type_repo.get_list_dried_larvae_discharge_types(
            page=page,
            page_size=page_size,
            search=search,
            is_active=is_active
        )
