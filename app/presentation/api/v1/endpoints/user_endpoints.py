from fastapi import APIRouter, status
from fastapi import Depends

from application.schemas.role_schemas import RoleDTO
from application.schemas.factory_schemas import FactoryDTO
from application.schemas.department_schemas import DepartmentDTO
from application.schemas.user_schemas import UserDTO
from presentation.schemas.user_dto import (
    ChangePasswordInputDTO,
    CreateUserInputDTO,
    UpdateStatusInputDTO,
    UpdateUserInputDTO,
)
from presentation.schemas.filter_dto import FilterDTO, PaginateDTO
from presentation.schemas.response import Response
from presentation.api.v1.dependencies.user_dependencies import (
    ChangePasswordUCDep,
    ChangeStatusUseCaseDep,
    CreateUserUseCaseDep,
    GetCurrentUserDep,
    GetMeUseCaseDep,
    TokenVerifyDep,
    GetListUserUseCaseDep,
    UpdateUserUseCaseDep,
)
from presentation.schemas.token_dto import TokenPayloadInputDTO

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model_exclude_none=True)
async def get_list_users(
    token: TokenVerifyDep,
    use_case: GetListUserUseCaseDep,
    filter_params: FilterDTO = Depends(),
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
        user_dto = UserDTO(
            id=user.id,
            email=user.email,
            phone=user.phone,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            department=DepartmentDTO(
                id=user.department_factory_role.department.id,
                name=user.department_factory_role.department.name,
                abbr_name=user.department_factory_role.department.abbr_name,
                description=user.department_factory_role.department.description,
                parent_id=user.department_factory_role.department.parent_id,
                is_active=user.department_factory_role.department.is_active,
            ),
            factory=FactoryDTO(
                id=user.department_factory_role.factory.id,
                name=user.department_factory_role.factory.name,
                abbr_name=user.department_factory_role.factory.abbr_name,
                description=user.department_factory_role.factory.description,
                is_active=user.department_factory_role.factory.is_active,
            ),
            role=RoleDTO(
                id=user.department_factory_role.role.id,
                name=user.department_factory_role.role.name,
                description=user.department_factory_role.role.description,
                is_active=user.department_factory_role.role.is_active,
            ),
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
    print(token_input_dto)
    user_dto = get_me_use_case.execute(user_id=token_input_dto.sub)

    return Response.success_response(
        code="ETB-lay_thong_tin_thanh_cong", data=user_dto
    ).get_dict()


@router.patch(
    "/{target_user_id}/password",
    summary="Change password",
    response_model_exclude_none=True,
)
async def change_password(
    token: TokenVerifyDep,
    body: ChangePasswordInputDTO,
    change_password_use_case: ChangePasswordUCDep,
    target_user: GetCurrentUserDep,
):
    print("actor_role_id", token.get("role_id"))
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
    body: UpdateStatusInputDTO,
    change_status_use_case: ChangeStatusUseCaseDep,
    target_user: GetCurrentUserDep,
):
    change_status_use_case.execute(status=body.status, target_user=target_user)

    return Response.success_response(
        code="ETB-thay_doi_trang_thai_thanh_cong", data="Success"
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
    body: CreateUserInputDTO,
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
    body: UpdateUserInputDTO,
    update_user_use_case: UpdateUserUseCaseDep,
    target_user: GetCurrentUserDep,
):
    update_user_use_case.execute(user_id=target_user.id, user_dto=body)

    return Response.success_response(
        code="ETB-cap_nhat_thong_tin_thanh_cong", data="Success"
    ).get_dict()
