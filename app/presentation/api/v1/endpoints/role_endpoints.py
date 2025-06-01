from fastapi import APIRouter, Depends, Path

from app.application.dto.role_dto import RoleDTO
from app.presentation.api.v1.dependencies.role_dependencies import (
    CreateRoleUCDep, ListRoleUCDep, UpdateRoleUCDep, UpdateStatusRoleUCDep)
from app.presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from app.presentation.schemas.filter_schema import FilterSchema, PaginateSchema
from app.presentation.schemas.response import Response
from app.presentation.schemas.role_schema import (CreateRoleSchema,
                                              UpdateRoleSchema,
                                              UpdateStatusRoleSchema)

router = APIRouter(prefix="/roles", tags=["Role"])


@router.get("/", response_model_exclude_none=True)
async def get_all_roles(
    token: TokenVerifyDep,
    use_case: ListRoleUCDep,
    filter_params: FilterSchema = Depends(),
):
    result = use_case.execute(
        page=filter_params.page,
        page_size=filter_params.page_size,
        search=filter_params.search,
        is_active=filter_params.is_active,
    )

    roles = []

    for role in result["items"]:
        role_dto = RoleDTO(
            id=role.id,
            name=role.name,
            description=role.description,
            is_active=role.is_active,
        )
        roles.append(role_dto)

    paginate_data = PaginateSchema(
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
        items=roles,
    )

    return Response.success_response(
        code="ETB-lay_danh_sach_vai_tro_thanh_cong", data=paginate_data
    ).get_dict()


@router.post("/", response_model_exclude_none=True)
async def create_role(
    token: TokenVerifyDep,
    body: CreateRoleSchema,
    use_case: CreateRoleUCDep,
):
    use_case.execute(role=body)

    return Response.success_response(
        code="ETB-tao_vai_tro_thanh_cong", data="success"
    ).get_dict()


@router.put("/{role_id}", response_model_exclude_none=True)
async def update_role(
    token: TokenVerifyDep,
    use_case: UpdateRoleUCDep,
    body: UpdateRoleSchema,
    role_id: int = Path(...),
):
    role = RoleDTO(
        id=role_id,
        name=body.name,
        description=body.description,
    )

    use_case.execute(role_dto=role)

    return Response.success_response(
        code="ETB-cap_nhat_vai_tro_thanh_cong", data="success"
    ).get_dict()


@router.patch("/{role_id}/status", response_model_exclude_none=True)
async def update_role_status(
    token: TokenVerifyDep,
    use_case: UpdateStatusRoleUCDep,
    body: UpdateStatusRoleSchema,
    role_id: int = Path(...),
):
    use_case.execute(role_id=role_id, is_active=body.is_active)

    return Response.success_response(
        code="ETB-cap_nhat_trang_thai_vai_tro_thanh_cong", data="success"
    ).get_dict()
