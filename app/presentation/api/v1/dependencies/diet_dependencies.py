from typing import Annotated

from fastapi import Depends
from application.use_cases.diet.list_diet_uc_impl import ListDietUC
from application.interfaces.use_cases.diet.list_diet_uc import IListDietUC
from infrastructure.database.repositories.diet_repository_impl import DietRepository
from domain.interfaces.repositories.diet_repository import IDietRepository
from presentation.api.v1.dependencies.common_dependencies import (
    DatabaseDep,
    QueryHelperDep,
)


def get_diet_repository(
    db: DatabaseDep, query_helper: QueryHelperDep
) -> IDietRepository:
    return DietRepository(conn=db, query_helper=query_helper)


def get_list_diet_uc(
    repository: Annotated[IDietRepository, Depends(get_diet_repository)],
) -> IListDietUC:
    return ListDietUC(diet_repository=repository)


ListDietUCDep = Annotated[IListDietUC, Depends(get_list_diet_uc)]
