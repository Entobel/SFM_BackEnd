from fastapi import APIRouter, Depends

from app.presentation.api.v1.dependencies.dryer_machine_type_dependencies import ListDryerMachineTypeUseCaseDep
from app.presentation.api.v1.dependencies.dryer_product_type_dependencies import ListDryerProductTypeUseCaseDep
from app.presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from app.presentation.schemas.dryer_machine_type_schema import DryerMachineTypeResponseSchema
from app.presentation.schemas.dryer_product_type_schema import DryerProductTypeResponseSchema
from app.presentation.schemas.filter_schema import FilterSchema, PaginateDTO
from app.presentation.schemas.response import Response

router = APIRouter(prefix="/dryer_product_types", tags=["Dryer Product Types"])


@router.get("/")
async def get_list_dryer_product_types(
        token_verify_dep: TokenVerifyDep,
        use_case: ListDryerProductTypeUseCaseDep,
        filter_params: FilterSchema = Depends()):

    result = use_case.execute(
        page=filter_params.page,
        page_size=filter_params.page_size,
        search=filter_params.search,
        is_active=filter_params.is_active
    )

    _dryer_product_types = result["items"]

    dryer_product_types = [
        DryerProductTypeResponseSchema(
            id=dpt.id,
            name=dpt.name,
            is_active=dpt.is_active,
            created_at=dpt.created_at,
            updated_at=dpt.updated_at
        ).model_dump(exclude_none=True)
        for dpt in _dryer_product_types
    ]

    paginate_schema = PaginateDTO(
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
        items=dryer_product_types,
    )

    return Response.success_response(
        code="ETB-lay_danh_sach_dryer_product_type_thanh_cong",
        data=paginate_schema
    ).get_dict()
