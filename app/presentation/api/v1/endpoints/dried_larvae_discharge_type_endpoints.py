from fastapi import APIRouter, Depends

from app.presentation.api.v1.dependencies.dried_larvae_discharge_type_dependencies import ListDriedLarvaeDischargeTypeUseCaseDep
from app.presentation.api.v1.dependencies.dryer_machine_type_dependencies import ListDryerMachineTypeUseCaseDep
from app.presentation.api.v1.dependencies.dryer_product_type_dependencies import ListDryerProductTypeUseCaseDep
from app.presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from app.presentation.schemas.dried_larvae_discharge_type_schema import DriedLarvaeDischargeTypeResponseSchema
from app.presentation.schemas.dryer_machine_type_schema import DryerMachineTypeResponseSchema
from app.presentation.schemas.dryer_product_type_schema import DryerProductTypeResponseSchema
from app.presentation.schemas.filter_schema import FilterSchema, PaginateDTO
from app.presentation.schemas.response import Response

router = APIRouter(prefix="/dried_larvae_discharge_types",
                   tags=["Dried Larvae Discharge Types"])


@router.get("/")
async def get_list_dried_larvae_discharge_types(
        token_verify_dep: TokenVerifyDep,
        use_case: ListDriedLarvaeDischargeTypeUseCaseDep,
        filter_params: FilterSchema = Depends()):

    result = use_case.execute(
        page=filter_params.page,
        page_size=filter_params.page_size,
        search=filter_params.search,
        is_active=filter_params.is_active
    )

    _dried_larvae_discharge_types = result["items"]

    dried_larvae_discharge_types = [
        DriedLarvaeDischargeTypeResponseSchema(
            id=dldt.id,
            name=dldt.name,
            is_active=dldt.is_active,
            created_at=dldt.created_at,
            updated_at=dldt.updated_at
        ).model_dump(exclude_none=True)
        for dldt in _dried_larvae_discharge_types
    ]

    paginate_schema = PaginateDTO(
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
        items=dried_larvae_discharge_types,
    )

    return Response.success_response(
        code="ETB-lay_danh_sach_dried_larvae_discharge_type_thanh_cong",
        data=paginate_schema
    ).get_dict()
