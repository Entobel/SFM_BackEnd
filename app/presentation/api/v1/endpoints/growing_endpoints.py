from re import I
from fastapi import APIRouter, Depends
from loguru import logger

from app.application.dto.diet_dto import DietDTO
from app.application.dto.factory_dto import FactoryDTO
from app.application.dto.growing_dto import GrowingDTO, UpdateGrowingDTO
from app.application.dto.produciton_type_dto import ProductionTypeDTO
from app.application.dto.production_object_dto import ProductionObjectDTO
from app.application.dto.shift_dto import ShiftDTO
from app.application.dto.user_dto import UserDTO
from app.application.dto.zone_dto import ZoneDTO
from app.application.dto.zone_level_dto import ZoneLevelDTO
from app.presentation.api.v1.dependencies.growing_dependencies import (
    CreateGrowingReportUseCaseDep,
    GetListGrowingReportUseCaseDep,
    UpdateGrowingReportUseCaseDep,
    UpdateStatusGrowingReportUseCaseDep,
)
from app.presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from app.presentation.schemas.diet_schema import DietResponseSchema
from app.presentation.schemas.factory_schema import FactoryResponseSchema
from app.presentation.schemas.filter_schema import FilterSchema, PaginateDTO
from app.presentation.schemas.growing_schema import (
    CreateGrowingSchema,
    GrowingResponseSchema,
    UpdateGrowingSchema,
    UpdateStatusGrowingSchema,
)
from app.presentation.schemas.growing_zone_level_schema import (
    GrowingZoneLevelResponseSchema,
)
from app.presentation.schemas.production_object_schema import (
    ProductionObjectResponseSchema,
)
from app.presentation.schemas.production_type_schema import ProductionTypeResponseSchema
from app.presentation.schemas.response import Response
from app.presentation.schemas.shift_schema import ShiftResponseSchema
from app.presentation.schemas.user_schema import UserResponseSchema
from app.presentation.schemas.zone_level_schema import ZoneLevelResponseSchema
from app.presentation.schemas.zone_schema import ZoneResponseSchema


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
        zone_leve_dto = ZoneLevelDTO(id=id, zone=ZoneDTO(id=body.zone_id))

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

    result = use_case.execute(
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

    [growings, growing_zone_levels, [growing_pending_count, growing_rejected_count]] = (
        result["items"]
    )

    growing_zone_level_map: dict[int,
                                 list[GrowingZoneLevelResponseSchema]] = {}

    for gzl in growing_zone_levels:
        gzl_schema = GrowingZoneLevelResponseSchema(
            id=gzl.id,
            status=gzl.status,
            snapshot_level_name=gzl.snapshot_level_name,
            snapshot_zone_number=gzl.snapshot_zone_number,
            zone_level=ZoneLevelResponseSchema(
                id=gzl.zone_level.id,
                zone=ZoneResponseSchema(id=gzl.zone_level.zone.id),
                status=gzl.zone_level.status
            ),
        ).model_dump(exclude_none=True)

        growing_id = gzl.growing.id
        growing_zone_level_map.setdefault(growing_id, []).append(gzl_schema)

    list_growing_response = [
        GrowingResponseSchema(
            id=g.id,
            date_produced=g.date_produced,
            shift=ShiftResponseSchema(
                id=g.shift.id,
                name=g.shift.name,
            ),
            production_type=ProductionTypeResponseSchema(
                id=g.production_type.id,
                name=g.production_type.name,
                description=g.production_type.description,
                abbr_name=g.production_type.abbr_name,
            ),
            production_object=ProductionObjectResponseSchema(
                id=g.production_object.id,
                name=g.production_object.name,
                description=g.production_object.description,
                abbr_name=g.production_object.abbr_name,
            ),
            diet=DietResponseSchema(
                id=g.diet.id,
                name=g.diet.name,
                description=g.diet.description,
            ),
            factory=FactoryResponseSchema(
                id=g.factory.id,
                name=g.factory.name,
                abbr_name=g.factory.abbr_name,
            ),
            assigned_zone_levels=growing_zone_level_map.get(g.id, []),
            substrate_moisture=g.substrate_moisture,
            number_crates=g.number_crates,
            notes=g.notes,
            is_active=g.is_active,
            status=g.status,
            created_by=UserResponseSchema(
                id=g.created_by.id,
                first_name=g.created_by.first_name,
                last_name=g.created_by.last_name,
                email=g.created_by.email,
                phone=g.created_by.phone,
            ),
            rejected_by=UserResponseSchema(
                id=g.rejected_by.id,
                first_name=g.rejected_by.first_name,
                last_name=g.rejected_by.last_name,
                email=g.rejected_by.email,
                phone=g.rejected_by.phone,
            ),
            rejected_at=g.rejected_at,
            rejected_reason=g.rejected_reason,
            approved_by=UserResponseSchema(
                id=g.approved_by.id,
                first_name=g.approved_by.first_name,
                last_name=g.approved_by.last_name,
                email=g.approved_by.email,
                phone=g.approved_by.phone,
            ),
            approved_at=g.approved_at,
            created_at=g.created_at,
            updated_at=g.updated_at,
        ).model_dump(exclude_none=True)
        for g in growings
    ]

    paginate_schema = PaginateDTO(
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
        items=list_growing_response,
    )

    return Response.success_response(
        code="ETB-lay_danh_sach_growing_report_thanh_cong",
        data={
            **paginate_schema.model_dump(),
            "counts": {
                "pending": growing_pending_count,
                "rejected": growing_rejected_count,
            },
        },
    ).get_dict()


@router.patch("/{growing_id}/status")
async def update_status_growing(
    token_verify: TokenVerifyDep,
    body: UpdateStatusGrowingSchema,
    growing_id: int,
    use_case: UpdateStatusGrowingReportUseCaseDep,
):

    use_case.execute(
        status=body.status,
        rejected_at=body.rejected_at,
        rejected_by=body.rejected_by,
        rejected_reason=body.rejected_reason,
        approved_at=body.approved_at,
        approved_by=body.approved_by,
        growing_id=growing_id,
    )

    return Response.success_response(
        data="Success", code="ETB_cap_nhat_trang_thai_growing_report_thanh_cong"
    ).get_dict()


@router.put("/{growing_id}")
async def update_growing_report(
    token_verify: TokenVerifyDep,
    body: UpdateGrowingSchema,
    growing_id: int,
    use_case: UpdateGrowingReportUseCaseDep
):
    growing_dto = UpdateGrowingDTO(
        id=growing_id,
        diet=DietDTO(id=body.diet_id),
        shift=ShiftDTO(id=body.shift_id),
        factory=FactoryDTO(id=body.factory_id),
        notes=body.notes,
        substrate_moisture=body.substrate_moisture,
        number_crates=body.number_crates,
        production_object=ProductionObjectDTO(id=body.production_object_id),
        production_type=ProductionTypeDTO(id=body.production_type_id),
        approved_at=body.approved_at,
        approved_by=UserDTO(id=body.approved_by),
        status=body.status,
    )

    use_case.execute(growing_dto=growing_dto, new_zone_level_ids=body.zone_level_ids,
                     old_zone_level_ids=body.old_zone_level_ids, old_zone_id=body.old_zone_id, new_zone_id=body.zone_id)

    return Response.success_response(
        data="Success", code="ETB_cap_nhat_growing_report_thanh_cong"
    ).get_dict()
