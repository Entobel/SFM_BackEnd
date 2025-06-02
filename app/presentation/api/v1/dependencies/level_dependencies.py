from typing import Annotated

from fastapi import Depends

from app.application.interfaces.use_cases.level.create_level_uc import ICreateLevelUC
from app.application.interfaces.use_cases.level.list_level_uc import IListLevelUC
from app.application.interfaces.use_cases.level.update_status_level_uc import IUpdateStatusLevelUC
from app.application.use_cases.level.create_level_uc_impl import CreateLevelUC
from app.application.use_cases.level.list_level_uc_impl import ListLevelUC
from app.application.use_cases.level.update_status_level_uc_impl import UpdateStatusLevelUC
from app.domain.interfaces.repositories.level_repository import ILevelRepository
from app.infrastructure.database.repositories.level_repository_impl import LevelRepository
from app.presentation.api.v1.dependencies.common_dependencies import (QueryHelperDep, DatabaseDep)


def get_level_repository(db: DatabaseDep, query_helper: QueryHelperDep) -> ILevelRepository:
    return LevelRepository(conn=db, query_helper=query_helper)


LevelRepositoryDep = Annotated[ILevelRepository, Depends(get_level_repository)]


def get_list_level_uc(level_repo: LevelRepositoryDep) -> IListLevelUC:
    return ListLevelUC(level_repo=level_repo)


def get_create_level_uc(level_repo: LevelRepositoryDep) -> ICreateLevelUC:
    return CreateLevelUC(level_repo=level_repo)


def get_update_level_uc(level_repo: LevelRepositoryDep) -> IUpdateStatusLevelUC:
    return UpdateStatusLevelUC(level_repo=level_repo)


GetListLevelUCDep = Annotated[IListLevelUC, Depends(get_list_level_uc)]
CreateLevelUCDep = Annotated[ICreateLevelUC, Depends(get_create_level_uc)]
UpdateStatusLevelUCDep = Annotated[IUpdateStatusLevelUC, Depends(get_update_level_uc)]
