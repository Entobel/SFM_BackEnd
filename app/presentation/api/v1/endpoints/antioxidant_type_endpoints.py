from fastapi import APIRouter, Depends

from app.presentation.api.v1.dependencies.antioxidant_type_dependencies import ListAntioxidantTypeUseCaseDep
from app.presentation.api.v1.dependencies.dryer_machine_type_dependencies import ListDryerMachineTypeUseCaseDep
from app.presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from app.presentation.schemas.antioxidant_schema import AntioxidantTypeResponseSchema
from app.presentation.schemas.dryer_machine_type_schema import DryerMachineTypeResponseSchema
from app.presentation.schemas.filter_schema import FilterSchema, PaginateDTO
from app.presentation.schemas.response import Response

router = APIRouter(prefix="/antioxidant_types", tags=["Antioxidant Types"])


@router.get("/")
async def get_list_antioxidant_types(
        token_verify_dep: TokenVerifyDep,
        use_case: ListAntioxidantTypeUseCaseDep,
        filter_params: FilterSchema = Depends()):

    result = use_case.execute(
        page=filter_params.page,
        page_size=filter_params.page_size,
        search=filter_params.search,
        is_active=filter_params.is_active
    )

    _antioxidant_types = result["items"]

    antioxidant_types = [
        AntioxidantTypeResponseSchema(
            id=at.id,
            name=at.name,
            is_active=at.is_active,
            created_at=at.created_at,
            updated_at=at.updated_at
        ).model_dump(exclude_none=True)
        for at in _antioxidant_types
    ]

    paginate_schema = PaginateDTO(
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
        items=antioxidant_types,
    )

    return Response.success_response(
        code="ETB-lay_danh_sach_antioxidant_type_thanh_cong",
        data=paginate_schema
    ).get_dict()
