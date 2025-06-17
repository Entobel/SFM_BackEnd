from fastapi import APIRouter
from loguru import logger

from app.application.dto.dd_dto import DDDTO
from app.application.dto.dryer_machine_type_dto import DryerMachineTypeDTO
from app.application.dto.factory_dto import FactoryDTO
from app.application.dto.shift_dto import ShiftDTO
from app.presentation.api.v1.dependencies.dd_dependencies import CreateDDReportUseCase
from app.presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from app.presentation.schemas.dd_schema import CreateDDSchema


router = APIRouter(prefix="/dds", tags=["Drum Drying"])


@router.post('/')
async def create_dd_report(token_verify_dep: TokenVerifyDep, body: CreateDDSchema, use_case: CreateDDReportUseCase):
    dd_dto = DDDTO(
        date_reported=body.date_reported,
        shift=ShiftDTO(id=body.shift_id),
        dried_larvae_discharge_type_id=body.dried_larvae_discharge_type_id,
        created_by=body.created_by,
        dryer_machine_type=DryerMachineTypeDTO(
            id=body.dryer_machine_type_id
        ),
        drying_results=body.drying_results,
        start_time=body.start_time,
        end_time=body.end_time,
        factory=FactoryDTO(
            id=body.factory_id
        ),
        quantity_dried_larvae_output=body.quantity_dried_larvae_output,
        quantity_fresh_larvae_input=body.quantity_fresh_larvae_input,
        temperature_after_2h=body.temperature_after_2h,
        temperature_after_3h=body.temperature_after_3h,
        temperature_after_3h30=body.temperature_after_3h30,
        temperature_after_4h=body.temperature_after_4h,
        temperature_after_4h30=body.temperature_after_4h30,
        notes=body.notes
    )

    use_case.execute(dd_dto=dd_dto)
