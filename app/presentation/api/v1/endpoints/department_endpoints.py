from application.schemas.department_factory_role_dto import DepartmentFactoryRoleDTO
from application.schemas.department_factory_dto import DepartmentFactoryDTO
from application.schemas.department_dto import DepartmentDTO
from application.schemas.factory_dto import FactoryDTO
from application.schemas.role_dto import RoleDTO
from fastapi import APIRouter, Depends
from presentation.api.v1.dependencies.department_dependencies import (
    CreateDepartmentFactoryRoleUseCaseDep,
    CreateDepartmentFactoryUseCaseDep,
    CreateDepartmentUseCaseDep,
    ListDepartmentFactoryRoleUseCaseDep,
    ListDepartmentFactoryUseCaseDep,
    ListDepartmentUseCaseDep,
    UpdateDepartmentUseCaseDep,
    UpdateStatusDepartmentFactoryRoleUseCaseDep,
    UpdateStatusDepartmentFactoryUseCaseDep,
    UpdateStatusDepartmentUseCaseDep,
)
from presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from presentation.schemas.department_dto import (
    CreateDepartmentDTO,
    UpdateDepartmentDTO,
    UpdateStatusDepartmentDTO,
)
from presentation.schemas.department_factory_dto import (
    CreateDepartmentFactoryDTO,
    UpdateStatusDepartmentFactoryDTO,
)
from presentation.schemas.department_factory_role_dto import (
    CreateDepartmentFactoryRoleDTO,
    DepartmentFactoryRoleDTOResponse,
    UpdateStatusDepartmentFactoryRoleDTO,
)
from presentation.schemas.filter_dto import FilterDTO, PaginateDTO
from presentation.schemas.response import Response

router = APIRouter(prefix="/departments", tags=["Department"])


@router.get("/", response_model_exclude_none=True)
async def get_all_department(
    token: TokenVerifyDep,
    use_case: ListDepartmentUseCaseDep,
    filter_params: FilterDTO = Depends(),
):
    result = use_case.execute(
        page=filter_params.page,
        page_size=filter_params.page_size,
        search=filter_params.search,
        is_active=filter_params.is_active,
    )

    departments = []

    for department in result["items"]:
        department_dto = DepartmentDTO(
            id=department.id,
            name=department.name,
            abbr_name=department.abbr_name,
            description=department.description,
            parent_id=department.parent_id,
            is_active=department.is_active,
        )
        departments.append(department_dto)

    paginate_data = PaginateDTO(
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
        items=departments,
    )

    return Response.success_response(
        code="ETB-lay_danh_sach_phong_ban_thanh_cong", data=paginate_data
    ).get_dict()


@router.post("/")
async def create_department(
    token: TokenVerifyDep,
    body: CreateDepartmentDTO,
    use_case: CreateDepartmentUseCaseDep,
):

    department = DepartmentDTO(
        name=body.name,
        abbr_name=body.abbr_name,
        description=body.description,
        parent_id=body.parent_id,
    )

    use_case.execute(department)

    return Response.success_response(
        code="ETB-tao_phong_ban_thanh_cong", data="Success"
    ).get_dict()


@router.put("/{department_id}", response_model_exclude_none=True)
async def update_department(
    token: TokenVerifyDep,
    department_id: int,
    body: UpdateDepartmentDTO,
    use_case: UpdateDepartmentUseCaseDep,
):
    department = DepartmentDTO(
        id=department_id,
        name=body.name,
        abbr_name=body.abbr_name,
        description=body.description,
        parent_id=body.parent_id,
    )

    use_case.execute(department_id, department)

    return Response.success_response(
        code="ETB-cap_nhat_phong_ban_thanh_cong", data="Success"
    ).get_dict()


@router.patch("/{department_id}/status", response_model_exclude_none=True)
async def update_status_department(
    token: TokenVerifyDep,
    department_id: int,
    body: UpdateStatusDepartmentDTO,
    use_case: UpdateStatusDepartmentUseCaseDep,
):
    use_case.execute(department_id, body.is_active)

    return Response.success_response(
        code="ETB-cap_nhat_trang_thai_phong_ban_thanh_cong", data="Success"
    ).get_dict()


@router.get("/department-factory", response_model_exclude_none=True)
async def get_department_factory(
    token: TokenVerifyDep,
    use_case: ListDepartmentFactoryUseCaseDep,
    filter_params: FilterDTO = Depends(),
):
    result = use_case.execute(
        page=filter_params.page,
        page_size=filter_params.page_size,
        search=filter_params.search,
        is_active=filter_params.is_active,
        department_id=filter_params.department_id,
        factory_id=filter_params.factory_id,
    )

    department_factories = []

    for department_factory in result["items"]:
        department_factory_dto = DepartmentFactoryDTO(
            id=department_factory.id,
            department=DepartmentDTO(
                id=department_factory.department.id,
                name=department_factory.department.name,
                abbr_name=department_factory.department.abbr_name,
                description=department_factory.department.description,
                parent_id=department_factory.department.parent_id,
                is_active=department_factory.department.is_active,
            ),
            factory=FactoryDTO(
                id=department_factory.factory.id,
                name=department_factory.factory.name,
                abbr_name=department_factory.factory.abbr_name,
                description=department_factory.factory.description,
                location=department_factory.factory.location,
                is_active=department_factory.factory.is_active,
            ),
            is_active=department_factory.is_active,
        )
        department_factories.append(department_factory_dto)

    paginate_data = PaginateDTO(
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
        items=department_factories,
    )

    return Response.success_response(
        code="ETB-lay_danh_sach_phong_ban_nha_may_thanh_cong", data=paginate_data
    ).get_dict()


# get list department factory role
@router.get("/department-factory-role", response_model_exclude_none=True)
async def get_department_factory_role(
    token: TokenVerifyDep,
    use_case: ListDepartmentFactoryRoleUseCaseDep,
    filter_params: FilterDTO = Depends(),
):
    result = use_case.execute(
        page=filter_params.page,
        page_size=filter_params.page_size,
        search=filter_params.search,
        is_active=filter_params.is_active,
        department_id=filter_params.department_id,
        factory_id=filter_params.factory_id,
    )

    department_factory_roles = []

    for department_factory_role in result["items"]:
        department_factory_role_dto = DepartmentFactoryRoleDTOResponse(
            id=department_factory_role.id,
            department=DepartmentDTO(
                id=department_factory_role.department_factory.department.id,
                name=department_factory_role.department_factory.department.name,
                abbr_name=department_factory_role.department_factory.department.abbr_name,
                description=department_factory_role.department_factory.department.description,
                parent_id=department_factory_role.department_factory.department.parent_id,
            ),
            factory=FactoryDTO(
                id=department_factory_role.department_factory.factory.id,
                name=department_factory_role.department_factory.factory.name,
                abbr_name=department_factory_role.department_factory.factory.abbr_name,
            ),
            role=RoleDTO(
                id=department_factory_role.role.id,
                name=department_factory_role.role.name,
            ),
            is_active=department_factory_role.is_active,
        )
        department_factory_roles.append(department_factory_role_dto)

    paginate_data = PaginateDTO(
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
        items=department_factory_roles,
    )

    return Response.success_response(
        code="ETB-lay_danh_sach_phong_ban_nha_may_vai_tro_thanh_cong",
        data=paginate_data,
    ).get_dict()


@router.post("/department-factory", response_model_exclude_none=True)
async def create_department_factory(
    token: TokenVerifyDep,
    body: CreateDepartmentFactoryDTO,
    use_case: CreateDepartmentFactoryUseCaseDep,
):
    factory_dto = FactoryDTO(
        id=body.factory_id,
    )

    department_dto = DepartmentDTO(
        id=body.department_id,
    )

    use_case.execute(factory_dto=factory_dto, department_dto=department_dto)

    return Response.success_response(
        code="ETB-tao_phong_ban_cua_nha_may_thanh_cong", data="Success"
    ).get_dict()


@router.patch(
    "/department-factory/{department_factory_id}/status",
    response_model_exclude_none=True,
)
async def update_status_department_factory(
    token: TokenVerifyDep,
    department_factory_id: int,
    body: UpdateStatusDepartmentFactoryDTO,
    use_case: UpdateStatusDepartmentFactoryUseCaseDep,
):
    department_factory_dto = DepartmentFactoryDTO(
        id=department_factory_id,
        is_active=body.is_active,
    )

    use_case.execute(department_factory_dto=department_factory_dto)

    return Response.success_response(
        code="ETB-cap_nhat_trang_thai_phong_ban_nha_may_thanh_cong", data="Success"
    ).get_dict()


@router.post("/department-factory-role", response_model_exclude_none=True)
async def create_department_factory_role(
    token: TokenVerifyDep,
    body: CreateDepartmentFactoryRoleDTO,
    use_case: CreateDepartmentFactoryRoleUseCaseDep,
):
    department_factory_role_dto = DepartmentFactoryRoleDTO(
        department_factory=DepartmentFactoryDTO(
            id=body.department_factory_id,
        ),
        role=RoleDTO(
            id=body.role_id,
        ),
    )

    use_case.execute(department_factory_role_dto=department_factory_role_dto)

    return Response.success_response(
        code="ETB-tao_phong_ban_cua_nha_may_vai_tro_thanh_cong", data="Success"
    ).get_dict()


@router.patch(
    "/department-factory-role/{department_factory_role_id}/status",
    response_model_exclude_none=True,
)
async def update_status_department_factory_role(
    token: TokenVerifyDep,
    department_factory_role_id: int,
    body: UpdateStatusDepartmentFactoryRoleDTO,
    use_case: UpdateStatusDepartmentFactoryRoleUseCaseDep,
):
    department_factory_role_dto = DepartmentFactoryRoleDTO(
        id=department_factory_role_id,
        is_active=body.is_active,
    )

    use_case.execute(department_factory_role_dto=department_factory_role_dto)

    return Response.success_response(
        code="ETB-cap_nhat_trang_thai_phong_ban_nha_may_vai_tro_thanh_cong",
        data="Success",
    ).get_dict()
