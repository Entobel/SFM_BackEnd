from typing import Annotated

from fastapi import Depends
from app.application.interfaces.use_cases.dryer_machine_type.list_dryer_machine_type_uc import IListDryerMachineTypeUC
from app.application.use_cases.dryer_machine_type.list_dryer_machine_type_uc_impl import ListDryerMachineTypeUC
from app.domain.interfaces.repositories.dryer_machine_type_repository import IDryerMachineTypeRepository
from app.infrastructure.database.repositories.dryer_machine_type_repository_impl import DryerMachineTypeRepository
from app.presentation.api.v1.dependencies.common_dependencies import DatabaseDep, QueryHelperDep


def get_dryer_machine_type_repository(conn: DatabaseDep, query_helper: QueryHelperDep) -> IDryerMachineTypeRepository:
    return DryerMachineTypeRepository(conn=conn, query_helper=query_helper)


DryerMachineTypeRepositoryDep = Annotated[IDryerMachineTypeRepository, Depends(
    get_dryer_machine_type_repository)]


def get_list_dryer_machine_type_uc(dryer_machine_repository: DryerMachineTypeRepositoryDep) -> IListDryerMachineTypeUC:
    return ListDryerMachineTypeUC(
        dryer_machine_repo=dryer_machine_repository
    )


ListDryerMachineTypeUseCaseDep = Annotated[IListDryerMachineTypeUC, Depends(
    get_list_dryer_machine_type_uc)]
