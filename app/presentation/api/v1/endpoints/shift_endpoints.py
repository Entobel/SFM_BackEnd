from fastapi import APIRouter

from presentation.schemas.response import Response
from presentation.api.v1.dependencies.shift_dependencies import ListShiftUCDep
from presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep


router = APIRouter(prefix="/shifts", tags=["Shift"])


@router.get("/")
async def get_all_shifts(
    token: TokenVerifyDep,
    list_shift_uc: ListShiftUCDep,
):

    shifts = list_shift_uc.execute()

    return Response.success_response(
        code="ETB_get_list_shift_success",
        data=shifts,
    ).get_dict()
