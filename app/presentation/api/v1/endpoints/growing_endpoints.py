from fastapi import APIRouter

from app.application.dto.diet_dto import DietDTO
from app.application.dto.factory_dto import FactoryDTO
from app.application.dto.growing_dto import GrowingDTO
from app.application.dto.produciton_type_dto import ProductionTypeDTO
from app.application.dto.production_object_dto import ProductionObjectDTO
from app.application.dto.shift_dto import ShiftDTO
from app.application.dto.zone_level_dto import ZoneLevelDTO
from app.domain.entities.user_entity import UserEntity
from app.presentation.api.v1.dependencies.growing_dependencies import (
    CreateGrowingReportUCDep,
)
from app.presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from app.presentation.schemas.growing_schema import CreateGrowingSchema
from app.presentation.schemas.response import Response


router = APIRouter(prefix="/growings", tags=["Growings"])


@router.post("/")
async def create_growing_report(
    token: TokenVerifyDep, body: CreateGrowingSchema, use_case: CreateGrowingReportUCDep
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
        user=UserEntity(id=body.created_by),
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
