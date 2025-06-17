from fastapi import APIRouter
from loguru import logger

from app.application.dto.dried_larvae_discharge_type_dto import DriedLarvaeDischargeTypeDTO
from app.application.dto.factory_dto import FactoryDTO
from app.application.dto.product_type_dto import ProductTypeDTO
from app.application.dto.shift_dto import ShiftDTO
from app.application.dto.user_dto import UserDTO
from app.application.dto.vfbd_dto import VfbdDTO
from app.presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from app.presentation.api.v1.dependencies.vfbd_dependencies import CreateVfbdReportUseCase
from app.presentation.schemas.response import Response
from app.presentation.schemas.vfbd_schema import CreateVFBDSchema


router = APIRouter(prefix="/vfbds", tags=["Vibratory Fluid Bed Drying"])


@router.post('/')
async def create_vfbd_report(
        token_verify_def: TokenVerifyDep,
        body: CreateVFBDSchema,
        use_case: CreateVfbdReportUseCase):

    vfbd_dto = VfbdDTO(
        date_reported=body.date_reported,
        shift=ShiftDTO(id=body.shift_id),
        factory=FactoryDTO(
            id=body.factory_id
        ),
        start_time=body.start_time,
        end_time=body.end_time,
        harvest_time=body.harvest_time,
        temperature_output_1st=body.temperature_output_1st,
        temperature_output_2nd=body.temperature_output_2nd,
        product_type=ProductTypeDTO(
            id=body.product_type_id
        ),
        dried_larvae_discharge_type=DriedLarvaeDischargeTypeDTO(
            id=body.dried_larvae_discharge_type_id
        ),
        quantity_dried_larvae_sold=body.quantity_dried_larvae_sold,
        dried_larvae_moisture=body.dried_larvae_moisture,
        drying_result=body.drying_result,
        notes=body.notes,
        created_by=UserDTO(id=body.created_by)
    )

    use_case.execute(vfbd_dto=vfbd_dto)

    return Response.success_response(
        data="Success", code="ETB_tao_vfbd_report_thanh_cong"
    ).get_dict()
