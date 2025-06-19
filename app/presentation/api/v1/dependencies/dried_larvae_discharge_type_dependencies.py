from typing import Annotated

from fastapi import Depends
from app.application.interfaces.use_cases.dried_larvae_discharge_type.list_dried_larvae_discharge_type_uc import IListDriedLarvaeDischargeTypeUC
from app.application.use_cases.dried_larvae_discharge_type.list_dried_larvae_discharge_type_uc_impl import ListDriedLarvaeDischargeTypeUC
from app.domain.interfaces.repositories.dried_larvae_discharge_type_repository import IDriedLarvaeDischargeTypeRepository
from app.infrastructure.database.repositories.dried_larvae_discharge_type_repository_impl import DriedLarvaeDischargeTypeRepository
from app.presentation.api.v1.dependencies.common_dependencies import DatabaseDep, QueryHelperDep


def get_dried_larvae_discharge_type_repository(conn: DatabaseDep, query_helper: QueryHelperDep) -> IDriedLarvaeDischargeTypeRepository:
    return DriedLarvaeDischargeTypeRepository(conn=conn, query_helper=query_helper)


DriedLarvaeDischargeTypeRepositoryDep = Annotated[IDriedLarvaeDischargeTypeRepository, Depends(
    get_dried_larvae_discharge_type_repository)]


def get_list_dried_larvae_discharge_type_uc(dried_larvae_discharge_type_repository: DriedLarvaeDischargeTypeRepositoryDep) -> IListDriedLarvaeDischargeTypeUC:
    return ListDriedLarvaeDischargeTypeUC(
        dried_larvae_discharge_type_repo=dried_larvae_discharge_type_repository
    )


ListDriedLarvaeDischargeTypeUseCaseDep = Annotated[IListDriedLarvaeDischargeTypeUC, Depends(
    get_list_dried_larvae_discharge_type_uc)]
