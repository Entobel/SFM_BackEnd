from typing import Annotated
from fastapi import Depends

from application.use_cases.department.update_status_department_uc_impl import (
    UpdateStatusDepartmentUC,
)
from application.interfaces.use_cases.department.update_status_department_uc import (
    IUpdateStatusDepartmentUC,
)
from application.use_cases.department.update_department_uc_impl import (
    UpdateDepartmentUC,
)
from application.interfaces.use_cases.department.update_department_uc import (
    IUpdateDepartmentUC,
)
from application.use_cases.department.create_department_uc_impl import (
    CreateDepartmentUC,
)
from application.interfaces.use_cases.department.create_department_uc import (
    ICreateDepartmentUC,
)
from application.interfaces.use_cases.department.list_department_uc import (
    IListDepartmentUC,
)
from infrastructure.database.repositories.department_repository_impl import (
    DepartmentRepository,
)
from presentation.api.v1.dependencies.common_dependencies import (
    DatabaseDep,
    QueryHelperDep,
)
from domain.interfaces.repositories.department_repository import IDepartmentRepository
from application.use_cases.department.list_department_uc_impl import ListDepartmentUC


def get_department_repository(
    conn: DatabaseDep,
    query_helper: QueryHelperDep,
) -> IDepartmentRepository:
    return DepartmentRepository(conn=conn, query_helper=query_helper)


def get_list_department_use_case(
    department_repository: Annotated[
        IDepartmentRepository, Depends(get_department_repository)
    ],
) -> IListDepartmentUC:
    return ListDepartmentUC(department_repository=department_repository)


def get_create_department_use_case(
    department_repository: Annotated[
        IDepartmentRepository, Depends(get_department_repository)
    ],
) -> ICreateDepartmentUC:
    return CreateDepartmentUC(department_repository=department_repository)


def get_update_department_use_case(
    department_repository: Annotated[
        IDepartmentRepository, Depends(get_department_repository)
    ],
) -> IUpdateDepartmentUC:
    return UpdateDepartmentUC(department_repository=department_repository)


def get_update_status_department_use_case(
    department_repository: Annotated[
        IDepartmentRepository, Depends(get_department_repository)
    ],
) -> IUpdateStatusDepartmentUC:
    return UpdateStatusDepartmentUC(department_repository=department_repository)


ListDepartmentUseCaseDep = Annotated[
    IListDepartmentUC, Depends(get_list_department_use_case)
]

CreateDepartmentUseCaseDep = Annotated[
    ICreateDepartmentUC, Depends(get_create_department_use_case)
]

UpdateDepartmentUseCaseDep = Annotated[
    IUpdateDepartmentUC, Depends(get_update_department_use_case)
]

UpdateStatusDepartmentUseCaseDep = Annotated[
    IUpdateStatusDepartmentUC, Depends(get_update_status_department_use_case)
]
