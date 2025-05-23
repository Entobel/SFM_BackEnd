from fastapi import APIRouter

from presentation.api.v1.dependencies.production_object_dependencies import (
    ListProductionObjectUCDep,
)
from presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from presentation.schemas.response import Response

router = APIRouter(prefix="/production-objects", tags=["Production Object"])


# List Production Objects
@router.get("/")
async def get_production_objects(
    token: TokenVerifyDep,
    use_case: ListProductionObjectUCDep,
):
    production_objects = use_case.execute()

    return Response.success_response(
        code="ETB_get_production_objects_success",
        data=production_objects,
    ).get_dict()
