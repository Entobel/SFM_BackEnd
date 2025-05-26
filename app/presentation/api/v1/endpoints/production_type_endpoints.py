from fastapi import APIRouter, Depends

from presentation.schemas.production_type_dto import (
    CreateProductionTypeDTO,
    UpdateProductionTypeDTO,
)
from application.schemas.produciton_type_schemas import ProductionTypeDTO
from presentation.schemas.filter_dto import FilterDTO, PaginateDTO
from presentation.api.v1.dependencies.production_type_denpendencies import (
    CreateProductionTypeUCDep,
    ListProductionTypeUCDep,
    UpdateProductionTypeUCDep,
)
from presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from presentation.schemas.response import Response

router = APIRouter(prefix="/production-types", tags=["Production Type"])


# Get list
@router.get("/")
async def get_production_types(
    token: TokenVerifyDep,
    use_case: ListProductionTypeUCDep,
    filter_params: FilterDTO = Depends(),
):
    result = use_case.execute(
        page=filter_params.page,
        page_size=filter_params.page_size,
        search=filter_params.search,
        is_active=filter_params.is_active,
    )

    production_types = []

    for production_type in result["items"]:
        production_types.append(
            ProductionTypeDTO(
                id=production_type.id,
                name=production_type.name,
                abbr_name=production_type.abbr_name,
                description=production_type.description,
                is_active=production_type.is_active,
            )
        )

    paginate_data = PaginateDTO(
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
        items=production_types,
    )

    return Response.success_response(
        code="ETB_get_production_types_success",
        data=paginate_data,
    ).get_dict()


# Create production type
@router.post("/")
async def create_production_type(
    token: TokenVerifyDep,
    use_case: CreateProductionTypeUCDep,
    body: CreateProductionTypeDTO,
):

    production_type_dto = ProductionTypeDTO(
        name=body.name,
        abbr_name=body.abbr_name,
        description=body.description,
    )

    use_case.execute(production_type_dto=production_type_dto)

    return Response.success_response(
        code="ETB-tao_loai_san_pham_thanh_cong",
        data="Success",
    ).get_dict()


# Update production type
@router.put("/{production_type_id}")
async def update_production_type(
    token: TokenVerifyDep,
    use_case: UpdateProductionTypeUCDep,
    production_type_id: int,
    body: UpdateProductionTypeDTO,
):
    production_type_dto = ProductionTypeDTO(
        id=production_type_id,
        name=body.name,
        abbr_name=body.abbr_name,
        description=body.description,
    )

    use_case.execute(production_type_dto=production_type_dto)

    return Response.success_response(
        code="ETB-cap_nhat_loai_san_pham_thanh_cong",
        data="Success",
    ).get_dict()
