from fastapi import APIRouter, Depends

from app.application.dto.production_object_dto import ProductionObjectDTO
from app.presentation.api.v1.dependencies.production_object_dependencies import (
    CreateProductionObjectUCDep,
    ListProductionObjectUCDep,
    UpdateProductionObjectUCDep,
    UpdateStatusProductionObjectUCDep,
)
from app.presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from app.presentation.schemas.filter_schema import FilterSchema, PaginateDTO
from app.presentation.schemas.production_object_schema import (
    CreateProductionObjectSchema,
    ProductionObjectResponseSchema,
    UpdateProductionObjectDTO,
    UpdateStatusProductionObjectSchema,
)
from app.presentation.schemas.response import Response

router = APIRouter(prefix="/production-objects", tags=["Production Object"])


# List Production Objects
@router.get("/")
async def get_production_objects(
    token: TokenVerifyDep,
    use_case: ListProductionObjectUCDep,
    filter_params: FilterSchema = Depends(),
):
    result = use_case.execute(
        page=filter_params.page,
        page_size=filter_params.page_size,
        search=filter_params.search,
        is_active=filter_params.is_active,
    )

    production_objects = []

    for production_object in result["items"]:
        production_objects.append(
            ProductionObjectResponseSchema(
                id=production_object.id,
                name=production_object.name,
                abbr_name=production_object.abbr_name,
                description=production_object.description,
                is_active=production_object.is_active,
            ).model_dump(exclude_none=True)
        )

    paginate_data = PaginateDTO(
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
        items=production_objects,
    )

    return Response.success_response(
        code="ETB_get_production_objects_success",
        data=paginate_data,
    ).get_dict()


@router.post("/")
async def create_production_object(
    token: TokenVerifyDep,
    use_case: CreateProductionObjectUCDep,
    body: CreateProductionObjectSchema,
):
    production_object_dto = ProductionObjectDTO(
        name=body.name,
        description=body.description,
    )

    use_case.execute(production_object_dto=production_object_dto)

    return Response.success_response(
        code="ETB_create_production_object_success",
        data="Success",
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
        data="Success",
    ).get_dict()


@router.patch("/{production_object_id}/status")
async def update_status_production_object(
    token: TokenVerifyDep,
    use_case: UpdateStatusProductionObjectUCDep,
    production_object_id: int,
    body: UpdateStatusProductionObjectSchema,
):
    production_object_dto = ProductionObjectDTO(
        id=production_object_id,
        is_active=body.is_active,
    )

    use_case.execute(production_object_dto=production_object_dto)

    return Response.success_response(
        code="ETB_update_status_production_object_success",
        data="Success",
    ).get_dict()
