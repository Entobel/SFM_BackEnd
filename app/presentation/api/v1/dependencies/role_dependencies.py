from typing import Annotated

from fastapi import Depends
from application.interfaces.use_cases.role.update_status_role_uc import (
    IUpdateStatusRoleUC,
)
from application.use_cases.role.update_role_status_uc_impl import UpdateRoleStatusUc
from application.use_cases.role.update_role_uc_impl import UpdateRoleUC
from application.interfaces.use_cases.role.update_role_uc import IUpdateRoleUC
from application.interfaces.use_cases.role.create_role_uc import ICreateRoleUC
from application.use_cases.role.create_role_uc_impl import CreateRoleUC
from application.interfaces.use_cases.role.list_role_uc import IListRoleUC
from application.use_cases.role.list_role_uc_impl import ListRoleUC
from domain.interfaces.repositories.role_repository import IRoleRepository
from infrastructure.database.repositories.role_repository_impl import RoleRepository
from presentation.api.v1.dependencies.common_dependencies import (
    DatabaseDep,
    QueryHelperDep,
)


def get_role_repository(
    db: DatabaseDep, query_helper: QueryHelperDep
) -> IRoleRepository:
    return RoleRepository(conn=db, query_helper=query_helper)


def get_list_role_uc(
    repo: Annotated[IRoleRepository, Depends(get_role_repository)],
) -> IListRoleUC:
    return ListRoleUC(role_repository=repo)


def get_create_role_uc(
    repo: Annotated[IRoleRepository, Depends(get_role_repository)],
) -> ICreateRoleUC:
    return CreateRoleUC(role_repository=repo)


def get_update_role_uc(
    repo: Annotated[IRoleRepository, Depends(get_role_repository)],
) -> IUpdateRoleUC:
    return UpdateRoleUC(role_repository=repo)


def get_update_status_role_uc(
    repo: Annotated[IRoleRepository, Depends(get_role_repository)],
) -> IUpdateStatusRoleUC:
    return UpdateRoleStatusUc(role_repo=repo)


ListRoleUCDep = Annotated[IListRoleUC, Depends(get_list_role_uc)]
CreateRoleUCDep = Annotated[ICreateRoleUC, Depends(get_create_role_uc)]
UpdateRoleUCDep = Annotated[IUpdateRoleUC, Depends(get_update_role_uc)]
UpdateStatusRoleUCDep = Annotated[
    IUpdateStatusRoleUC, Depends(get_update_status_role_uc)
]
