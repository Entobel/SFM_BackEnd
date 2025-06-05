from typing import Annotated

from fastapi import Depends

from app.application.interfaces.use_cases.department.create_department_factory_role_uc import (
    ICreateDepartmentFactoryRoleUC,
)
from app.application.interfaces.use_cases.department.create_department_factory_uc import (
    ICreateDepartmentFactoryUC,
)
from app.application.interfaces.use_cases.department.create_department_uc import (
    ICreateDepartmentUC,
)
from app.application.interfaces.use_cases.department.list_department_factory_role_uc import (
    IListDepartmentFactoryRoleUC,
)
from app.application.interfaces.use_cases.department.list_department_factory_uc import (
    IListDepartmentFactoryUC,
)
from app.application.interfaces.use_cases.department.list_department_uc import (
    IListDepartmentUC,
)
from app.application.interfaces.use_cases.department.update_department_uc import (
    IUpdateDepartmentUC,
)
from app.application.interfaces.use_cases.department.update_status_department_factory_role_uc import (
    IUpdateStatusDepartmentFactoryRoleUC,
)
from app.application.interfaces.use_cases.department.update_status_department_factory_uc import (
    IUpdateStatusDepartmentFactoryUC,
)
from app.application.interfaces.use_cases.department.update_status_department_uc import (
    IUpdateStatusDepartmentUC,
)
from app.application.use_cases.department.create_department_factory_role_uc_impl import (
    CreateDepartmentFactoryRoleUC,
)
from app.application.use_cases.department.create_department_factory_uc_impl import (
    CreateDepartmentFactoryUC,
)
from app.application.use_cases.department.create_department_uc_impl import (
    CreateDepartmentUC,
)
from app.application.use_cases.department.list_department_factory_role_uc_impl import (
    ListDepartmentFactoryRoleUC,
)
from app.application.use_cases.department.list_department_factory_uc_impl import (
    ListDepartmentFactoryUC,
)
from app.application.use_cases.department.list_department_uc_impl import (
    ListDepartmentUC,
)
from app.application.use_cases.department.update_department_uc_impl import (
    UpdateDepartmentUC,
)
from app.application.use_cases.department.update_status_department_factory_role_uc_impl import (
    UpdateStatusDepartmentFactoryRoleUC,
)
from app.application.use_cases.department.update_status_department_factory_uc_impl import (
    UpdateStatusDepartmentFactoryUC,
)
from app.application.use_cases.department.update_status_department_uc_impl import (
    UpdateStatusDepartmentUC,
)
from app.domain.interfaces.repositories.deparment_factory_role_repository import (
    IDepartmentFactoryRoleRepository,
)
from app.domain.interfaces.repositories.department_factory_repository import (
    IDepartmentFactoryRepository,
)
from app.domain.interfaces.repositories.department_repository import (
    IDepartmentRepository,
)
from app.domain.interfaces.repositories.role_repository import IRoleRepository
from app.infrastructure.database.repositories.department_factory_repository_impl import (
    DepartmentFactoryRepository,
)
from app.infrastructure.database.repositories.department_factory_role_repository_impl import (
    DepartmentFactoryRoleRepository,
)
from app.infrastructure.database.repositories.department_repository_impl import (
    DepartmentRepository,
)
from app.presentation.api.v1.dependencies.common_dependencies import (
    DatabaseDep,
    QueryHelperDep,
)
from app.presentation.api.v1.dependencies.factory_dependencies import (
    FactoryRepositoryDep,
)
from app.presentation.api.v1.dependencies.role_dependencies import get_role_repository


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
