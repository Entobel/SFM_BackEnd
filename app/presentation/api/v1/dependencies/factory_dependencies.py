from typing import Annotated

from fastapi import Depends

from application.interfaces.use_cases.factory.create_factory_uc import \
    ICreateFactoryUC
from application.interfaces.use_cases.factory.list_factory_uc import \
    IListFactoryUC
from application.interfaces.use_cases.factory.update_factory_uc import \
    IUpdateFactoryUC
from application.interfaces.use_cases.factory.update_status_factory_uc import \
    IUpdateStatusFactoryUC
from application.use_cases.factory.create_factory_uc_impl import \
    CreateFactoryUC
from application.use_cases.factory.list_factory_uc_impl import \
    ListFactoryUCImpl
from application.use_cases.factory.update_factory_uc_impl import \
    UpdateFactoryUC
from application.use_cases.factory.update_status_factory_uc_impl import \
    UpdateStatusFactoryUC
from domain.interfaces.repositories.factory_repository import \
    IFactoryRepository
from infrastructure.database.repositories.factory_repository_impl import \
    FactoryRepository
from presentation.api.v1.dependencies.common_dependencies import (
    DatabaseDep, QueryHelperDep)


def get_factory_repository(
    db: DatabaseDep, query_helper: QueryHelperDep
) -> IFactoryRepository:
    return FactoryRepository(conn=db, query_helper=query_helper)


FactoryRepositoryDep = Annotated[IFactoryRepository, Depends(get_factory_repository)]


def get_list_factory_use_case(
    repo: FactoryRepositoryDep,
) -> IListFactoryUC:
    return ListFactoryUCImpl(factory_repository=repo)


def get_create_factory_use_case(
    repo: FactoryRepositoryDep,
) -> ICreateFactoryUC:
    return CreateFactoryUC(factory_repository=repo)


def get_update_factory_use_case(
    repo: FactoryRepositoryDep,
) -> IUpdateFactoryUC:
    return UpdateFactoryUC(factory_repository=repo)


def get_update_status_factory_use_case(
    repo: FactoryRepositoryDep,
) -> IUpdateStatusFactoryUC:
    return UpdateStatusFactoryUC(factory_repository=repo)


ListFactoryUseCaseDep = Annotated[IListFactoryUC, Depends(get_list_factory_use_case)]
CreateFactoryUseCaseDep = Annotated[
    ICreateFactoryUC, Depends(get_create_factory_use_case)
]
UpdateFactoryUseCaseDep = Annotated[
    IUpdateFactoryUC, Depends(get_update_factory_use_case)
]
UpdateStatusFactoryUseCaseDep = Annotated[
    IUpdateStatusFactoryUC, Depends(get_update_status_factory_use_case)
]
