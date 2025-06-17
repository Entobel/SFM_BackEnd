from fastapi import APIRouter, Depends

from app.application.dto.operation_type_dto import OperationTypeDTO
from app.presentation.api.v1.dependencies.operation_type_denpendencies import (
    CreateOperationTypeUCDep, ListOperationTypeUCDep,
    UpdateOperationTypeUCDep, UpdateStatusOperationTypeUCDep)
from app.presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from app.presentation.schemas.filter_schema import FilterSchema, PaginateDTO
from app.presentation.schemas.operation_type_schema import (
    CreateOperationTypeSchema, UpdateOperationTypeSchema,
    UpdateStatusOperationTypeSchema)
from app.presentation.schemas.response import Response

router = APIRouter(prefix="/operation-types", tags=["Operation Type"])


# Get list
@router.get("/")
async def get_operation_types(
    token: TokenVerifyDep,
    use_case: ListOperationTypeUCDep,
    filter_params: FilterSchema = Depends(),
):
    result = use_case.execute(
        page=filter_params.page,
        page_size=filter_params.page_size,
        search=filter_params.search,
        is_active=filter_params.is_active,
    )

    operation_types = []

    for operation_type in result["items"]:
        operation_types.append(
            OperationTypeDTO(
                id=operation_type.id,
                name=operation_type.name,
                abbr_name=operation_type.abbr_name,
                description=operation_type.description,
                is_active=operation_type.is_active,
            )
        )

    paginate_data = PaginateDTO(
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
        items=operation_types,
    )

    return Response.success_response(
        code="ETB_get_operation_types_success",
        data=paginate_data,
    ).get_dict()


# Create production type
@router.post("/")
async def create_operation_type(
    token: TokenVerifyDep,
    use_case: CreateOperationTypeUCDep,
    body: CreateOperationTypeSchema,
):

    operation_type_dto = OperationTypeDTO(
        name=body.name,
        abbr_name=body.abbr_name,
        description=body.description,
    )

    use_case.execute(operation_type_dto=operation_type_dto)

    return Response.success_response(
        code="ETB-tao_loai_san_pham_thanh_cong",
        data="Success",
    ).get_dict()


# Update production type
@router.put("/{operation_type_id}")
async def update_operation_type(
    token: TokenVerifyDep,
    use_case: UpdateOperationTypeUCDep,
    operation_type_id: int,
    body: UpdateOperationTypeSchema,
):
    operation_type_dto = OperationTypeDTO(
        id=operation_type_id,
        name=body.name,
        abbr_name=body.abbr_name,
        description=body.description,
    )

    use_case.execute(operation_type_dto=operation_type_dto)

    return Response.success_response(
        code="ETB-cap_nhat_loai_san_pham_thanh_cong",
        data="Success",
    ).get_dict()


# Update status production type
@router.patch("/{operation_type_id}/status")
async def update_status_operation_type(
    token: TokenVerifyDep,
    use_case: UpdateStatusOperationTypeUCDep,
    operation_type_id: int,
    body: UpdateStatusOperationTypeSchema,
):
    operation_type_dto = OperationTypeDTO(
        id=operation_type_id,
        is_active=body.is_active,
    )

    use_case.execute(operation_type_dto=operation_type_dto)

    return Response.success_response(
        code="ETB-cap_nhat_trang_thai_loai_san_pham_thanh_cong",
        data="Success",
    ).get_dict()
