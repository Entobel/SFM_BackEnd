from fastapi import APIRouter, Depends


from app.presentation.api.v1.dependencies.packing_type_dependencies import ListPackingTypeUseCaseDep
from app.presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from app.presentation.schemas.filter_schema import FilterSchema, PaginateDTO
from app.presentation.schemas.packing_type_schema import PackingTypeResponseSchema
from app.presentation.schemas.response import Response
from app.presentation.schemas.unit_schema import UnitResponseSchema

router = APIRouter(prefix="/packing_types", tags=["Packing Types"])


@router.get("/")
async def get_list_packing_types(
        token_verify_dep: TokenVerifyDep,
        use_case: ListPackingTypeUseCaseDep,
        filter_params: FilterSchema = Depends()):

    result = use_case.execute(
        page=filter_params.page,
        page_size=filter_params.page_size,
        search=filter_params.search,
        is_active=filter_params.is_active
    )

    _packing_types = result["items"]

    packing_types = [
        PackingTypeResponseSchema(
            id=pt.id,
            name=pt.name,
            is_active=pt.is_active,
            quantity=pt.quantity,
            created_at=pt.created_at,
            updated_at=pt.updated_at,
            unit=UnitResponseSchema(
                id=pt.unit.id,
                symbol=pt.unit.symbol,
                multiplier_to_base=pt.unit.multiplier_to_base,
                unit_type=pt.unit.unit_type,
                is_active=pt.unit.is_active,
                created_at=pt.unit.created_at,
                updated_at=pt.unit.updated_at
            )
        ).model_dump(exclude_none=True)
        for pt in _packing_types
    ]

    paginate_schema = PaginateDTO(
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
        items=packing_types,
    )

    return Response.success_response(
        code="ETB-lay_danh_sach_packing_type_thanh_cong",
        data=paginate_schema
    ).get_dict()
