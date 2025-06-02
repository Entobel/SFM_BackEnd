from fastapi import APIRouter, Depends, status

from app.application.dto.department_dto import DepartmentDTO
from app.application.dto.factory_dto import FactoryDTO
from app.application.dto.role_dto import RoleDTO
from app.presentation.api.v1.dependencies.user_dependencies import (
    ChangePasswordUCDep,
    ChangeStatusUseCaseDep,
    CreateUserUseCaseDep,
    GetCurrentUserDep,
    GetListUserUseCaseDep,
    GetMeUseCaseDep,
    TokenVerifyDep,
    UpdateUserUseCaseDep,
)
from app.presentation.schemas.filter_schema import FilterSchema, PaginateDTO
from app.presentation.schemas.response import Response
from app.presentation.schemas.token_schema import TokenPayloadInputDTO
from app.presentation.schemas.user_schema import (
    ChangePasswordInputSchema,
    CreateUserInputSchema,
    UpdateStatusInputSchema,
    UpdateUserInputSchema,
    UserResponseSchema,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model_exclude_none=True)
async def get_list_users(
    token: TokenVerifyDep,
    use_case: GetListUserUseCaseDep,
    filter_params: FilterSchema = Depends(),
):
    result = use_case.execute(
        page=filter_params.page,
        page_size=filter_params.page_size,
        search=filter_params.search,
        department_id=filter_params.department_id,
        factory_id=filter_params.factory_id,
        role_id=filter_params.role_id,
        is_active=filter_params.is_active,
    )

    users = []

    for user in result["items"]:
        user_dto = UserResponseSchema(
            id=user.id,
            email=user.email,
            phone=user.phone,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            department=DepartmentDTO(
                id=user.department_factory_role.department_factory.department.id,
                name=user.department_factory_role.department_factory.department.name,
                abbr_name=user.department_factory_role.department_factory.department.abbr_name,
                description=user.department_factory_role.department_factory.department.description,
                parent_id=user.department_factory_role.department_factory.department.parent_id,
                is_active=user.department_factory_role.department_factory.department.is_active,
            ),
            factory=FactoryDTO(
                id=user.department_factory_role.department_factory.factory.id,
                name=user.department_factory_role.department_factory.factory.name,
                abbr_name=user.department_factory_role.department_factory.factory.abbr_name,
                description=user.department_factory_role.department_factory.factory.description,
                is_active=user.department_factory_role.department_factory.factory.is_active,
            ),
            role=RoleDTO(
                id=user.department_factory_role.role.id,
                name=user.department_factory_role.role.name,
                description=user.department_factory_role.role.description,
                is_active=user.department_factory_role.role.is_active,
            ),
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        users.append(user_dto)

    paginate_data = PaginateDTO(
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
        items=users,
    )

    return Response.success_response(
        code="ETB-lay_danh_sach_thanh_cong", data=paginate_data
    ).get_dict()


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Get own profile",
    response_model=None,
)
async def get_me(token: TokenVerifyDep, get_me_use_case: GetMeUseCaseDep):
    token_input_dto = TokenPayloadInputDTO(**token)

    user = get_me_use_case.execute(user_id=token_input_dto.sub)

    return Response.success_response(
        code="ETB-lay_thong_tin_thanh_cong", data=user
    ).get_dict()


# Create User
@router.post(
    "/",
    summary="Create User",
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    token: TokenVerifyDep,
    body: CreateUserInputSchema,
    create_user_use_case: CreateUserUseCaseDep,
):

    create_user_use_case.execute(user_dto=body)

    return Response.success_response(
        code="ETB-tao_tai_khoan_thanh_cong", data="Success"
    ).get_dict()


# Update User
@router.put(
    "/{target_user_id}",
    summary="Update User",
    response_model_exclude_none=True,
)
async def update_user(
    token: TokenVerifyDep,
    body: UpdateUserInputSchema,
    update_user_use_case: UpdateUserUseCaseDep,
    target_user: GetCurrentUserDep,
):
    update_user_use_case.execute(user_id=target_user.id, user_dto=body)

    return Response.success_response(
        code="ETB-cap_nhat_thong_tin_thanh_cong", data="Success"
    ).get_dict()


@router.patch(
    "/{target_user_id}/password",
    summary="Change password",
    response_model_exclude_none=True,
)
async def change_password(
    token: TokenVerifyDep,
    body: ChangePasswordInputSchema,
    change_password_use_case: ChangePasswordUCDep,
    target_user: GetCurrentUserDep,
):
    change_password_use_case.execute(
        target_user=target_user,
        old_password=body.old_password,
        new_password=body.new_password,
        actor_role_id=token.get("role_id"),
    )

    return Response.success_response(
        code="ETB-doi_mat_khau_thanh_cong", data="Success"
    ).get_dict()


@router.patch(
    "/{target_user_id}/status",
    summary="Change status user",
    response_model_exclude_none=True,
)
async def change_status_user(
    token: TokenVerifyDep,
    body: UpdateStatusInputSchema,
    change_status_use_case: ChangeStatusUseCaseDep,
    target_user: GetCurrentUserDep,
):
    change_status_use_case.execute(status=body.status, target_user=target_user)

    return Response.success_response(
        code="ETB-thay_doi_trang_thai_thanh_cong", data="Success"
    ).get_dict()
