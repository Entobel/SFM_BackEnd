from fastapi import APIRouter

from application.schemas.production_object_schemas import ProductionObjectDTO
from presentation.schemas.production_object_dto import (
    CreateProductionObjectDTO,
    UpdateProductionObjectDTO,
    UpdateStatusProductionObjectDTO,
)
from presentation.api.v1.dependencies.production_object_dependencies import (
    CreateProductionObjectUCDep,
    ListProductionObjectUCDep,
    UpdateProductionObjectUCDep,
    UpdateStatusProductionObjectUCDep,
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


@router.post("/")
async def create_production_object(
    token: TokenVerifyDep,
    use_case: CreateProductionObjectUCDep,
    body: CreateProductionObjectDTO,
):
    production_object_dto = ProductionObjectDTO(
        name=body.name,
        description=body.description,
    )

    use_case.execute(production_object_dto=production_object_dto)

    return Response.success_response(
        code="ETB_create_production_object_success",
    ).get_dict()


@router.put("/{production_object_id}")
async def update_production_object(
    token: TokenVerifyDep,
    use_case: UpdateProductionObjectUCDep,
    production_object_id: int,
    body: UpdateProductionObjectDTO,
):
    production_object_dto = ProductionObjectDTO(
        id=production_object_id,
        name=body.name,
        description=body.description,
    )

    use_case.execute(production_object_dto=production_object_dto)

    return Response.success_response(
        code="ETB_update_production_object_success",
    ).get_dict()


@router.patch("/{production_object_id}/status")
async def update_status_production_object(
    token: TokenVerifyDep,
    use_case: UpdateStatusProductionObjectUCDep,
    production_object_id: int,
    body: UpdateStatusProductionObjectDTO,
):
    production_object_dto = ProductionObjectDTO(
        id=production_object_id,
        is_active=body.is_active,
    )

    use_case.execute(production_object_dto=production_object_dto)

    return Response.success_response(
        code="ETB_update_status_production_object_success",
    ).get_dict()
