from fastapi import APIRouter, Depends

from app.application.dto.antioxidant_type_dto import AntioxidantTypeDTO
from app.application.dto.factory_dto import FactoryDTO
from app.application.dto.grinding_dto import GrindingDTO
from app.application.dto.packing_type_dto import PackingTypeDTO
from app.application.dto.shift_dto import ShiftDTO
from app.application.dto.user_dto import UserDTO
from app.presentation.api.v1.dependencies.grinding_dependencies import CreateGrindingUCDep
from app.presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from app.presentation.schemas.grinding_schema import CreateGrindingSchema
from app.presentation.schemas.response import Response

router = APIRouter(prefix="/grindings", tags=["Grinding"])

# Get List Grinding


@router.get("/")
async def get_list_grinding_report(token_verify_dep: TokenVerifyDep): ...

# Create Grinding Report


@router.post("/")
async def create_grinding_report(token_verify_dep: TokenVerifyDep,
                                 body: CreateGrindingSchema,
                                 use_case: CreateGrindingUCDep):
    grinding_dto = GrindingDTO(
        date_reported=body.date_reported,
        antioxidant_type=AntioxidantTypeDTO(
            id=body.antioxidant_type_id
        ),
        packing_type=PackingTypeDTO(id=body.packing_type_id),
        quantity=body.quantity,
        batch_grinding_information=body.batch_grinding_information,
        factory=FactoryDTO(
            id=body.factory_id
        ),
        notes=body.notes,
        shift=ShiftDTO(
            id=body.shift_id
        ),
        user=UserDTO(
            id=body.created_by
        )
    )

    use_case.execute(grinding_dto=grinding_dto)

    return Response.success_response(
        data="Success", code="ETB_tao_growing_report_thanh_cong"
    ).get_dict()
