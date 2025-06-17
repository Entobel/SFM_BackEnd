from typing import Annotated

from fastapi import Depends

from app.application.interfaces.use_cases.operation_type.create_operation_type_uc import (
    ICreateOperationTypeUC,
)
from app.application.interfaces.use_cases.operation_type.list_operation_type_uc import (
    IListOperationTypeUC,
)
from app.application.interfaces.use_cases.operation_type.update_operation_type_uc import (
    IUpdateOperationTypeUC,
)
from app.application.interfaces.use_cases.operation_type.update_status_operation_type_uc import (
    IUpdateStatusOperationTypeUC,
)
from app.application.use_cases.operation_type.create_operation_type_uc_impl import (
    CreateOperationTypeUC,
)
from app.application.use_cases.operation_type.list_operation_type_uc_impl import (
    ListOperationTypeUC,
)
from app.application.use_cases.operation_type.update_operation_type_uc_impl import (
    UpdateOperationTypeUC,
)
from app.application.use_cases.operation_type.update_status_operation_type_uc_impl import (
    UpdateStatusOperationTypeUC,
)
from app.domain.interfaces.repositories.operation_type_repository import (
    IOperationTypeRepository,
)
from app.infrastructure.database.repositories.operation_type_repository_impl import (
    OperationTypeRepository,
)
from app.presentation.api.v1.dependencies.common_dependencies import (
    DatabaseDep,
    QueryHelperDep,
)


def get_operation_type_repository(db: DatabaseDep, query_helper: QueryHelperDep):
    return OperationTypeRepository(conn=db, query_helper=query_helper)


OperationTypeRepositoryDep = Annotated[
    IOperationTypeRepository, Depends(get_operation_type_repository)
]


def get_operation_type_uc(
    repo: OperationTypeRepositoryDep,
) -> IListOperationTypeUC:
    return ListOperationTypeUC(repo=repo)


def get_create_operation_type_uc(
    repo: OperationTypeRepositoryDep,
) -> ICreateOperationTypeUC:
    return CreateOperationTypeUC(repo=repo)


def get_update_operation_type_uc(
    repo: OperationTypeRepositoryDep,
) -> IUpdateOperationTypeUC:
    return UpdateOperationTypeUC(repo=repo)


def get_update_status_operation_type_uc(
    repo: OperationTypeRepositoryDep,
) -> IUpdateStatusOperationTypeUC:
    return UpdateStatusOperationTypeUC(repo=repo)


ListOperationTypeUCDep = Annotated[
    IListOperationTypeUC, Depends(get_operation_type_uc)
]
CreateOperationTypeUCDep = Annotated[
    ICreateOperationTypeUC, Depends(get_create_operation_type_uc)
]
UpdateOperationTypeUCDep = Annotated[
    IUpdateOperationTypeUC, Depends(get_update_operation_type_uc)
]
UpdateStatusOperationTypeUCDep = Annotated[
    IUpdateStatusOperationTypeUC, Depends(
        get_update_status_operation_type_uc)
]
