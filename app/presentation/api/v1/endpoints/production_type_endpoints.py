from fastapi import APIRouter

from presentation.api.v1.dependencies.production_type_denpendencies import (
    ProductionTypeUCDep,
)
from presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from presentation.schemas.response import Response

router = APIRouter(prefix="/production-types", tags=["Production Type"])


@router.get("/")
async def get_production_types(
    token: TokenVerifyDep,
    use_case: ProductionTypeUCDep,
):
    production_types = use_case.execute()

    return Response.success_response(
        code="ETB_get_production_types_success",
        data=production_types,
    ).get_dict()
