from typing import Annotated

from fastapi import Depends

from app.application.interfaces.use_cases.diet.create_diet_uc import ICreateDietUC
from app.application.interfaces.use_cases.diet.list_diet_uc import IListDietUC
from app.application.interfaces.use_cases.diet.update_diet_uc import IUpdateDietUC
from app.application.interfaces.use_cases.diet.update_status_diet_uc import (
    IUpdateStatusDietUC,
)
from app.application.use_cases.diet.create_diet_uc_impl import CreateDietUC
from app.application.use_cases.diet.list_diet_uc_impl import ListDietUC
from app.application.use_cases.diet.update_diet_uc_impl import UpdateDietUC
from app.application.use_cases.diet.update_status_diet_uc_impl import UpdateStatusDietUC
from app.domain.interfaces.repositories.diet_repository import IDietRepository
from app.infrastructure.database.repositories.diet_repository_impl import DietRepository
from app.presentation.api.v1.dependencies.common_dependencies import (
    DatabaseDep,
    QueryHelperDep,
)


def get_diet_repository(
    db: DatabaseDep, query_helper: QueryHelperDep
) -> IDietRepository:
    return DietRepository(conn=db, query_helper=query_helper)


DietRepositoryDep = Annotated[IDietRepository, Depends(get_diet_repository)]


def get_list_diet_uc(
    repository: DietRepositoryDep,
) -> IListDietUC:
    return ListDietUC(diet_repository=repository)


def get_create_diet_uc(
    repository: DietRepositoryDep,
) -> ICreateDietUC:
    return CreateDietUC(diet_repository=repository)


def get_update_status_diet_uc(
    repository: DietRepositoryDep,
) -> IUpdateStatusDietUC:
    return UpdateStatusDietUC(diet_repository=repository)


def get_update_diet_uc(
    repository: DietRepositoryDep,
) -> IUpdateDietUC:
    return UpdateDietUC(diet_repository=repository)


ListDietUCDep = Annotated[IListDietUC, Depends(get_list_diet_uc)]
CreateDietUCDep = Annotated[ICreateDietUC, Depends(get_create_diet_uc)]
UpdateDietStatusUCDep = Annotated[
    IUpdateStatusDietUC, Depends(get_update_status_diet_uc)
]
UpdateDietUCDep = Annotated[IUpdateDietUC, Depends(get_update_diet_uc)]
