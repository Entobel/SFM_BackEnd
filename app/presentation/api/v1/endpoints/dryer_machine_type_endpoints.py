from fastapi import APIRouter, Depends

from app.presentation.api.v1.dependencies.dryer_machine_type_dependencies import ListDryerMachineTypeUseCaseDep
from app.presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from app.presentation.schemas.dryer_machine_type_schema import DryerMachineTypeResponseSchema
from app.presentation.schemas.filter_schema import FilterSchema, PaginateDTO
from app.presentation.schemas.response import Response

router = APIRouter(prefix="/dryer_machine_types", tags=["Dryer Machine Types"])


@router.get("/")
async def get_list_dryer_machine_types(
        token_verify_dep: TokenVerifyDep,
        use_case: ListDryerMachineTypeUseCaseDep,
        filter_params: FilterSchema = Depends()):

    result = use_case.execute(
        page=filter_params.page,
        page_size=filter_params.page_size,
        search=filter_params.search,
        is_active=filter_params.is_active
    )

    _dryer_machine_types = result["items"]

    dryer_machine_types = [
        DryerMachineTypeResponseSchema(
            id=dmt.id,
            name=dmt.name,
            abbr_name=dmt.abbr_name,
            description=dmt.description,
            is_active=dmt.is_active,
            created_at=dmt.created_at,
            updated_at=dmt.updated_at
        ).model_dump(exclude_none=True)
        for dmt in _dryer_machine_types
    ]

    paginate_schema = PaginateDTO(
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
        items=dryer_machine_types,
    )

    return Response.success_response(
        code="ETB-lay_danh_sach_dryer_machine_type_thanh_cong",
        data=paginate_schema
    ).get_dict()
