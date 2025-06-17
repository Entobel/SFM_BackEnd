from fastapi import APIRouter, Depends
from loguru import logger

from app.application.dto.factory_dto import FactoryDTO
from app.application.dto.growing_dto import GrowingDTO
from app.application.dto.harvesting_dto import HarvestingDTO
from app.application.dto.shift_dto import ShiftDTO
from app.application.dto.user_dto import UserDTO
from app.application.dto.zone_dto import ZoneDTO
from app.application.dto.zone_level_dto import ZoneLevelDTO
from app.presentation.api.v1.dependencies.harvesting_dependencies import CreateHarvestingReportUseCaseDep, GetListHarvestingReportUseCaseDep
from app.presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from app.presentation.schemas.factory_schema import FactoryResponseSchema
from app.presentation.schemas.filter_schema import FilterSchema, PaginateDTO
from app.presentation.schemas.harvesting_schema import CreateHarvestingSchema, HarvestingResponseSchema
from app.presentation.schemas.harvesting_zone_level_schema import HarvestingZoneLevelResponseSchema
from app.presentation.schemas.response import Response
from app.presentation.schemas.shift_schema import ShiftResponseSchema
from app.presentation.schemas.user_schema import UserResponseSchema
from app.presentation.schemas.zone_level_schema import ZoneLevelResponseSchema
from app.presentation.schemas.zone_schema import ZoneResponseSchema

router = APIRouter(prefix="/harvestings", tags=["Harvestings"])


@router.post("/")
async def create_harvesting_report(
    token: TokenVerifyDep,
    body: CreateHarvestingSchema,
    use_case: CreateHarvestingReportUseCaseDep
):
    harvesting_dto = HarvestingDTO(
        date_harvested=body.date_harvested,
        factory=FactoryDTO(id=body.factory_id),
        shift=ShiftDTO(id=body.shift_id),
        notes=body.notes,
        number_crates=body.number_crates,
        number_crates_discarded=body.number_crates_discarded,
        quantity_larvae=body.quantity_larvae,
        created_by=UserDTO(id=body.created_by)
    )

    list_zone_level_dtos: list[ZoneLevelDTO] = []

    for id in body.zone_level_ids:
        zone_level_dto = ZoneLevelDTO(id=id, zone=ZoneDTO(id=body.zone_id))

        list_zone_level_dtos.append(zone_level_dto)

    use_case.execute(harvesting_dto=harvesting_dto,
                     zone_id=body.zone_id, zone_level_dtos=list_zone_level_dtos)

    return Response.success_response(
        data="Success", code="ETB_tao_harvesting_report_thanh_cong"
    ).get_dict()


@router.get("/")
async def get_list_harvesting_report(
    token: TokenVerifyDep,
    use_case: GetListHarvestingReportUseCaseDep,
    filter_params: FilterSchema = Depends(),
):

    result = use_case.execute(
        page=filter_params.page,
        page_size=filter_params.page_size,
        factory_id=filter_params.factory_id,
        is_active=filter_params.is_active,
        start_date=filter_params.start_date,
        end_date=filter_params.end_date,
        report_status=filter_params.report_status,
        search=filter_params.search,
    )

    [harvestings, harvesting_zone_levels, [harvesting_pending_count, harvesting_rejected_count]] = (
        result["items"]
    )

    harvesting_zone_level_map: dict[int,
                                    list[HarvestingZoneLevelResponseSchema]] = {}

    for hzl in harvesting_zone_levels:
        hzl_schema = HarvestingZoneLevelResponseSchema(
            id=hzl.id,
            status=hzl.status,
            snapshot_level_name=hzl.snapshot_level_name,
            snapshot_zone_number=hzl.snapshot_zone_number,
            zone_level=ZoneLevelResponseSchema(
                id=hzl.zone_level.id,
                zone=ZoneResponseSchema(id=hzl.zone_level.zone.id),
                status=hzl.zone_level.status
            ),
        ).model_dump(exclude_none=True)

        harvesting_id = hzl.harvesting.id
        harvesting_zone_level_map.setdefault(
            harvesting_id, []).append(hzl_schema)

    list_harvesting_response = [
        HarvestingResponseSchema(
            id=h.id,
            date_harvested=h.date_harvested,
            shift=ShiftResponseSchema(
                id=h.shift.id,
                name=h.shift.name,
            ),
            factory=FactoryResponseSchema(
                id=h.factory.id,
                name=h.factory.name,
                abbr_name=h.factory.abbr_name,
            ),
            assigned_zone_levels=harvesting_zone_level_map.get(
                h.id, []),
            number_crates=h.number_crates,
            number_crates_discarded=h.number_crates_discarded,
            quantity_larvae=h.quantity_larvae,
            notes=h.notes,
            is_active=h.is_active,
            status=h.status,
            created_by=UserResponseSchema(
                id=h.created_by.id,
                first_name=h.created_by.first_name,
                last_name=h.created_by.last_name,
                email=h.created_by.email,
                phone=h.created_by.phone,
            ),
            rejected_by=UserResponseSchema(
                id=h.rejected_by.id,
                first_name=h.rejected_by.first_name,
                last_name=h.rejected_by.last_name,
                email=h.rejected_by.email,
                phone=h.rejected_by.phone,
            ),
            rejected_at=h.rejected_at,
            rejected_reason=h.rejected_reason,
            approved_by=UserResponseSchema(
                id=h.approved_by.id,
                first_name=h.approved_by.first_name,
                last_name=h.approved_by.last_name,
                email=h.approved_by.email,
                phone=h.approved_by.phone,
            ),
            approved_at=h.approved_at,
            created_at=h.created_at,
            updated_at=h.updated_at,
        ).model_dump(exclude_none=True)
        for h in harvestings
    ]

    paginate_schema = PaginateDTO(
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
        items=list_harvesting_response,
    )

    return Response.success_response(
        code="ETB-lay_danh_sach_harvesting_report_thanh_cong",
        data={
            **paginate_schema.model_dump(),
            "counts": {
                "pending": harvesting_pending_count,
                "rejected": harvesting_rejected_count,
            },
        },
    ).get_dict()
