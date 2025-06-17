from fastapi import APIRouter, Depends

from app.application.dto.product_type_dto import ProductTypeDTO
from app.presentation.api.v1.dependencies.product_type_dependencies import (
    CreateProductTypeUCDep,
    ListProductTypeUCDep,
    UpdateProductTypeUCDep,
    UpdateStatusProductTypeUCDep,
)
from app.presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from app.presentation.schemas.filter_schema import FilterSchema, PaginateDTO
from app.presentation.schemas.product_type_schema import (
    CreateProductTypeSchema,
    ProductTypeResponseSchema,
    UpdateProductTypeDTO,
    UpdateStatusProductTypeSchema,
)
from app.presentation.schemas.response import Response

router = APIRouter(prefix="/production-objects", tags=["Production Object"])


# List Production Objects
@router.get("/")
async def get_product_types(
    token: TokenVerifyDep,
    use_case: ListProductTypeUCDep,
    filter_params: FilterSchema = Depends(),
):
    result = use_case.execute(
        page=filter_params.page,
        page_size=filter_params.page_size,
        search=filter_params.search,
        is_active=filter_params.is_active,
    )

    product_types = []

    for product_type in result["items"]:
        product_types.append(
            ProductTypeResponseSchema(
                id=product_type.id,
                name=product_type.name,
                abbr_name=product_type.abbr_name,
                description=product_type.description,
                is_active=product_type.is_active,
            ).model_dump(exclude_none=True)
        )

    paginate_data = PaginateDTO(
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
        items=product_types,
    )

    return Response.success_response(
        code="ETB_get_product_types_success",
        data=paginate_data,
    ).get_dict()


@router.post("/")
async def create_product_type(
    token: TokenVerifyDep,
    use_case: CreateProductTypeUCDep,
    body: CreateProductTypeSchema,
):
    product_type_dto = ProductTypeDTO(
        name=body.name,
        description=body.description,
    )

    use_case.execute(product_type_dto=product_type_dto)

    return Response.success_response(
        code="ETB_create_product_type_success",
        data="Success",
    ).get_dict()


@router.put("/{product_type_id}")
async def update_product_type(
    token: TokenVerifyDep,
    use_case: UpdateProductTypeUCDep,
    product_type_id: int,
    body: UpdateProductTypeDTO,
):
    product_type_dto = ProductTypeDTO(
        id=product_type_id,
        name=body.name,
        description=body.description,
    )

    use_case.execute(product_type_dto=product_type_dto)

    return Response.success_response(
        code="ETB_update_product_type_success",
        data="Success",
    ).get_dict()


@router.patch("/{product_type_id}/status")
async def update_status_product_type(
    token: TokenVerifyDep,
    use_case: UpdateStatusProductTypeUCDep,
    product_type_id: int,
    body: UpdateStatusProductTypeSchema,
):
    product_type_dto = ProductTypeDTO(
        id=product_type_id,
        is_active=body.is_active,
    )

    use_case.execute(product_type_dto=product_type_dto)

    return Response.success_response(
        code="ETB_update_status_product_type_success",
        data="Success",
    ).get_dict()
