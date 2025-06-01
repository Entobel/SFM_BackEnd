from typing import Annotated

from fastapi import Depends

from app.application.interfaces.use_cases.growing.create_growing_uc import \
    ICreateGrowingUC
from app.application.interfaces.use_cases.growing.list_growing_uc import \
    IListGrowingUC
from app.application.use_cases.growing.create_growing_uc_impl import \
    CreateGrowingUC
from app.application.use_cases.growing.list_growing_uc_impl import ListGrowingUC
from app.domain.interfaces.repositories.growing_repository import \
    IGrowingRepository
from app.infrastructure.database.repositories.growing_repository_impl import \
    GrowingRepository
from app.presentation.api.v1.dependencies.common_dependencies import (
    DatabaseDep, QueryHelperDep)


def get_grow_repository(
    db: DatabaseDep, query_helper: QueryHelperDep
) -> IGrowingRepository:
    return GrowingRepository(conn=db, query_helper=query_helper)


def get_list_growing_uc(
    grow_repository: Annotated[IGrowingRepository, Depends(get_grow_repository)],
) -> IListGrowingUC:
    return ListGrowingUC(growing_repository=grow_repository)


def create_growing_uc(
    grow_repository: Annotated[IGrowingRepository, Depends(get_grow_repository)],
) -> ICreateGrowingUC:
    return CreateGrowingUC(growing_repository=grow_repository)


ListGrowingUCDep = Annotated[IListGrowingUC, Depends(get_list_growing_uc)]
CreateGrowingUCDep = Annotated[ICreateGrowingUC, Depends(create_growing_uc)]
