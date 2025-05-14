from fastapi import APIRouter, Depends

from presentation.schemas.department_dto import (
    CreateDepartmentDTO,
    UpdateDepartmentDTO,
    UpdateStatusDepartmentDTO,
)
from presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from presentation.schemas.response import Response
from application.schemas.department_schemas import DepartmentDTO
from presentation.schemas.filter_dto import FilterDTO, PaginateDTO
from presentation.api.v1.dependencies.department_dependencies import (
    CreateDepartmentUseCaseDep,
    ListDepartmentUseCaseDep,
    UpdateDepartmentUseCaseDep,
    UpdateStatusDepartmentUseCaseDep,
)


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


@router.post("/", response_model_exclude_none=True)
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
