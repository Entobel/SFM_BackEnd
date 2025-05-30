from fastapi import APIRouter, Depends

from application.dto.shift_dto import ShiftDTO
from presentation.api.v1.dependencies.shift_dependencies import (
    CreateShiftUCDep, ListShiftUCDep, UpdateShiftUCDep, UpdateStatusShiftUCDep)
from presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from presentation.schemas.filter_schema import FilterSchema, PaginateSchema
from presentation.schemas.response import Response
from presentation.schemas.shift_schema import (CreateShiftSchema,
                                               UpdateShiftSchema,
                                               UpdateStatusShiftSchema)

router = APIRouter(prefix="/shifts", tags=["Shift"])


@router.get("/")
async def get_all_shifts(
    token: TokenVerifyDep,
    list_shift_uc: ListShiftUCDep,
    filter_params: FilterSchema = Depends(),
):

    result = list_shift_uc.execute(
        page=filter_params.page,
        page_size=filter_params.page_size,
        search=filter_params.search,
        is_active=filter_params.is_active,
    )

    shifts = []

    for shift in result["items"]:
        shift_dto = ShiftDTO(
            id=shift.id,
            name=shift.name,
            description=shift.description,
            is_active=shift.is_active,
        )
        shifts.append(shift_dto)

    paginate_data = PaginateSchema(
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
        items=shifts,
    )

    return Response.success_response(
        code="ETB_get_list_shift_success",
        data=paginate_data,
    ).get_dict()


@router.post("/")
def create_shift(
    token: TokenVerifyDep,
    use_case: CreateShiftUCDep,
    body: CreateShiftSchema,
):
    shift_dto = ShiftDTO(
        name=body.name,
        description=body.description,
    )

    use_case.execute(shift_dto=shift_dto)

    return Response.success_response(
        code="ETB-tao_shift_thanh_cong",
        data="Success",
    ).get_dict()


@router.patch("/{shift_id}/status")
def update_shift_status(
    token: TokenVerifyDep,
    use_case: UpdateStatusShiftUCDep,
    shift_id: int,
    body: UpdateStatusShiftSchema,
):
    shift_dto = ShiftDTO(
        id=shift_id,
        is_active=body.is_active,
    )

    use_case.execute(shift_dto=shift_dto)

    return Response.success_response(
        code="ETB-cap_nhat_trang_thai_shift_thanh_cong",
        data="Success",
    ).get_dict()


@router.put("/{shift_id}")
def update_shift(
    token: TokenVerifyDep,
    use_case: UpdateShiftUCDep,
    shift_id: int,
    body: UpdateShiftSchema,
):
    shift_dto = ShiftDTO(
        id=shift_id,
        description=body.description,
        name=body.name,
    )

    use_case.execute(shift_dto=shift_dto)

    return Response.success_response(
        code="ETB-cap_nhat_shift_thanh_cong",
        data="Success",
    ).get_dict()
