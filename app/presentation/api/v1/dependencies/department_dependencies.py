from typing import Annotated

from application.interfaces.use_cases.department.create_department_factory_role_uc import \
    ICreateDepartmentFactoryRoleUC
from application.interfaces.use_cases.department.create_department_factory_uc import \
    ICreateDepartmentFactoryUC
from application.interfaces.use_cases.department.create_department_uc import \
    ICreateDepartmentUC
from application.interfaces.use_cases.department.list_department_factory_role_uc import \
    IListDepartmentFactoryRoleUC
from application.interfaces.use_cases.department.list_department_factory_uc import \
    IListDepartmentFactoryUC
from application.interfaces.use_cases.department.list_department_uc import \
    IListDepartmentUC
from application.interfaces.use_cases.department.update_department_uc import \
    IUpdateDepartmentUC
from application.interfaces.use_cases.department.update_status_department_factory_role_uc import \
    IUpdateStatusDepartmentFactoryRoleUC
from application.interfaces.use_cases.department.update_status_department_factory_uc import \
    IUpdateStatusDepartmentFactoryUC
from application.interfaces.use_cases.department.update_status_department_uc import \
    IUpdateStatusDepartmentUC
from application.use_cases.department.create_department_factory_role_uc_impl import \
    CreateDepartmentFactoryRoleUC
from application.use_cases.department.create_department_factory_uc_impl import \
    CreateDepartmentFactoryUC
from application.use_cases.department.create_department_uc_impl import \
    CreateDepartmentUC
from application.use_cases.department.list_department_factory_role_uc_impl import \
    ListDepartmentFactoryRoleUC
from application.use_cases.department.list_department_factory_uc_impl import \
    ListDepartmentFactoryUC
from application.use_cases.department.list_department_uc_impl import \
    ListDepartmentUC
from application.use_cases.department.update_department_uc_impl import \
    UpdateDepartmentUC
from application.use_cases.department.update_status_department_factory_role_uc_impl import \
    UpdateStatusDepartmentFactoryRoleUC
from application.use_cases.department.update_status_department_factory_uc_impl import \
    UpdateStatusDepartmentFactoryUC
from application.use_cases.department.update_status_department_uc_impl import \
    UpdateStatusDepartmentUC
from domain.interfaces.repositories.deparment_factory_role_repository import \
    IDepartmentFactoryRoleRepository
from domain.interfaces.repositories.department_factory_repository import \
    IDepartmentFactoryRepository
from domain.interfaces.repositories.department_repository import \
    IDepartmentRepository
from domain.interfaces.repositories.role_repository import IRoleRepository
from fastapi import Depends
from infrastructure.database.repositories.department_factory_repository_impl import \
    DepartmentFactoryRepository
from infrastructure.database.repositories.department_factory_role_repository_impl import \
    DepartmentFactoryRoleRepository
from infrastructure.database.repositories.department_repository_impl import \
    DepartmentRepository
from presentation.api.v1.dependencies.common_dependencies import (
    DatabaseDep, QueryHelperDep)
from presentation.api.v1.dependencies.factory_dependencies import \
    FactoryRepositoryDep
from presentation.api.v1.dependencies.role_dependencies import \
    get_role_repository


def get_department_repository(
    conn: DatabaseDep,
    query_helper: QueryHelperDep,
) -> IDepartmentRepository:
    return DepartmentRepository(conn=conn, query_helper=query_helper)


DepartmentRepositoryDep = Annotated[
    IDepartmentRepository, Depends(get_department_repository)
]


def get_department_factory_repository(
    conn: DatabaseDep,
    query_helper: QueryHelperDep,
) -> IDepartmentFactoryRepository:
    return DepartmentFactoryRepository(conn=conn, query_helper=query_helper)


def get_list_department_use_case(
    department_repository: DepartmentRepositoryDep,
) -> IListDepartmentUC:
    return ListDepartmentUC(department_repository=department_repository)


def get_create_department_use_case(
    department_repository: DepartmentRepositoryDep,
) -> ICreateDepartmentUC:
    return CreateDepartmentUC(department_repository=department_repository)


def get_update_department_use_case(
    department_repository: DepartmentRepositoryDep,
) -> IUpdateDepartmentUC:
    return UpdateDepartmentUC(department_repository=department_repository)


def get_update_status_department_use_case(
    department_repository: DepartmentRepositoryDep,
) -> IUpdateStatusDepartmentUC:
    return UpdateStatusDepartmentUC(department_repository=department_repository)


def get_department_factory_role_repository(
    conn: DatabaseDep,
    query_helper: QueryHelperDep,
) -> IDepartmentFactoryRoleRepository:
    return DepartmentFactoryRoleRepository(conn=conn, query_helper=query_helper)


def get_list_department_factory_use_case(
    department_factory_repository: Annotated[
        IDepartmentFactoryRepository, Depends(get_department_factory_repository)
    ],
) -> IListDepartmentFactoryUC:
    return ListDepartmentFactoryUC(repository=department_factory_repository)


def get_list_department_factory_role_use_case(
    department_factory_role_repository: Annotated[
        IDepartmentFactoryRoleRepository,
        Depends(get_department_factory_role_repository),
    ],
) -> IListDepartmentFactoryRoleUC:
    return ListDepartmentFactoryRoleUC(repository=department_factory_role_repository)


def get_create_department_factory_use_case(
    department_repository: DepartmentRepositoryDep,
    factory_repository: FactoryRepositoryDep,
    department_factory_repository: Annotated[
        IDepartmentFactoryRepository, Depends(get_department_factory_repository)
    ],
) -> ICreateDepartmentFactoryUC:
    return CreateDepartmentFactoryUC(
        department_repo=department_repository,
        factory_repo=factory_repository,
        department_factory_repo=department_factory_repository,
    )


def get_update_status_department_factory_use_case(
    department_factory_repository: Annotated[
        IDepartmentFactoryRepository, Depends(get_department_factory_repository)
    ],
) -> IUpdateStatusDepartmentFactoryUC:
    return UpdateStatusDepartmentFactoryUC(
        department_factory_repo=department_factory_repository
    )


def get_create_department_factory_role_use_case(
    department_factory_role_repository: Annotated[
        IDepartmentFactoryRoleRepository,
        Depends(get_department_factory_role_repository),
    ],
    role_repository: Annotated[IRoleRepository, Depends(get_role_repository)],
) -> ICreateDepartmentFactoryRoleUC:
    return CreateDepartmentFactoryRoleUC(
        department_factory_role_repository=department_factory_role_repository,
        role_repository=role_repository,
    )


def get_update_status_department_factory_role_use_case(
    department_factory_role_repository: Annotated[
        IDepartmentFactoryRoleRepository,
        Depends(get_department_factory_role_repository),
    ],
) -> IUpdateStatusDepartmentFactoryRoleUC:
    return UpdateStatusDepartmentFactoryRoleUC(
        department_factory_role_repository=department_factory_role_repository
    )


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

ListDepartmentFactoryUseCaseDep = Annotated[
    IListDepartmentFactoryUC, Depends(get_list_department_factory_use_case)
]

ListDepartmentFactoryRoleUseCaseDep = Annotated[
    IListDepartmentFactoryRoleUC, Depends(get_list_department_factory_role_use_case)
]

CreateDepartmentFactoryUseCaseDep = Annotated[
    ICreateDepartmentFactoryUC, Depends(get_create_department_factory_use_case)
]

UpdateStatusDepartmentFactoryUseCaseDep = Annotated[
    IUpdateStatusDepartmentFactoryUC,
    Depends(get_update_status_department_factory_use_case),
]

CreateDepartmentFactoryRoleUseCaseDep = Annotated[
    ICreateDepartmentFactoryRoleUC, Depends(get_create_department_factory_role_use_case)
]

UpdateStatusDepartmentFactoryRoleUseCaseDep = Annotated[
    IUpdateStatusDepartmentFactoryRoleUC,
    Depends(get_update_status_department_factory_role_use_case),
]
