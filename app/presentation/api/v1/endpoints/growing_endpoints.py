from fastapi import APIRouter, Depends

from app.application.dto.diet_dto import DietDTO
from app.application.dto.factory_dto import FactoryDTO
from app.application.dto.growing_dto import GrowingDTO
from app.application.dto.produciton_type_dto import ProductionTypeDTO
from app.application.dto.production_object_dto import ProductionObjectDTO
from app.application.dto.shift_dto import ShiftDTO
from app.application.dto.user_dto import UserDTO
from app.application.dto.zone_level_dto import ZoneLevelDTO
from app.presentation.api.v1.dependencies.growing_dependencies import (
    CreateGrowingReportUseCaseDep,
    GetListGrowingReportUseCaseDep,
)
from app.presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from app.presentation.schemas.filter_schema import FilterSchema
from app.presentation.schemas.growing_schema import CreateGrowingSchema
from app.presentation.schemas.response import Response


router = APIRouter(prefix="/growings", tags=["Growings"])


@router.post("/")
async def create_growing_report(
    token: TokenVerifyDep,
    body: CreateGrowingSchema,
    use_case: CreateGrowingReportUseCaseDep,
):
    growing_dto = GrowingDTO(
        date_produced=body.date_produced,
        diet=DietDTO(id=body.diet_id),
        factory=FactoryDTO(id=body.factory_id),
        production_object=ProductionObjectDTO(id=body.production_object_id),
        production_type=ProductionTypeDTO(id=body.production_type_id),
        shift=ShiftDTO(id=body.shift_id),
        notes=body.notes,
        number_crates=body.number_crates,
        substrate_moisture=body.substrate_moisture,
        user=UserDTO(id=body.created_by),
    )

    list_zone_level_dtos: list[ZoneLevelDTO] = []

    for id in body.zone_level_ids:
        zone_leve_dto = ZoneLevelDTO(id=id)

        list_zone_level_dtos.append(zone_leve_dto)

    use_case.execute(
        zone_id=body.zone_id,
        growing_dto=growing_dto,
        zone_level_dtos=list_zone_level_dtos,
    )

    return Response.success_response(
        data="Success", code="ETB_tao_grow_report_thanh_cong"
    ).get_dict()


@router.get("/")
async def get_list_growing_report(
    token: TokenVerifyDep,
    use_case: GetListGrowingReportUseCaseDep,
    filter_params: FilterSchema = Depends(),
):

    use_case.execute(
        page=filter_params.page,
        page_size=filter_params.page_size,
        diet_id=filter_params.diet_id,
        factory_id=filter_params.factory_id,
        production_object_id=filter_params.production_object_id,
        production_type_id=filter_params.production_type_id,
        is_active=filter_params.is_active,
        start_date=filter_params.start_date,
        end_date=filter_params.end_date,
        report_status=filter_params.report_status,
        search=filter_params.search,
        substrate_moisture_lower_bound=filter_params.substrate_moisture_lower_bound,
        substrate_moisture_upper_bound=filter_params.substrate_moisture_upper_bound,
    )

    return True
