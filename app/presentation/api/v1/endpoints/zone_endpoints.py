from fastapi import APIRouter, Depends

from app.application.dto.factory_dto import FactoryDTO
from app.application.dto.zone_dto import ZoneDTO, ZoneResponseDTO
from app.application.dto.zone_level_dto import ZoneLevelDTO
from app.presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from app.presentation.api.v1.dependencies.zone_dependencies import (
    CreateZoneUseCaseDep,
    GetListZoneUseCaseDep,
    UpdateStatusZoneLevelUseCaseDep,
    UpdateStatusZoneUseCaseDep,
    UpdateZoneUseCaseDep,
)
from app.presentation.schemas.filter_schema import FilterSchema, PaginateDTO
from app.presentation.schemas.response import Response
from app.presentation.schemas.zone_schema import (
    CreateZoneSchema,
    UpdateStatusLevelZoneSchema,
    UpdateStatusZoneSchema,
    UpdateZoneSchema,
)

router = APIRouter(prefix="/zones", tags=["Zones"])


@router.get("/")
async def get_list_zones(
    token: TokenVerifyDep,
    use_case: GetListZoneUseCaseDep,
    filter_params: FilterSchema = Depends(),
):
    result = use_case.execute(
        page=filter_params.page,
        page_size=filter_params.page_size,
        search=filter_params.search,
        is_active=filter_params.is_active,
        factory_id=filter_params.factory_id,
    )

    zone_level_entities = result["items"][0]
    zone_entities = result["items"][1]

    zone_level_map: dict[int, list[ZoneLevelDTO]] = {}

    for zl in zone_level_entities:
        dto = ZoneLevelDTO(
            id=zl.id,
            level=zl.level,
            is_active=zl.is_active,
            created_at=zl.created_at,
            updated_at=zl.updated_at,
        )
        zone_id = zl.zone.id
        zone_level_map.setdefault(zone_id, []).append(dto)

    zones: list[ZoneDTO] = []

    for zone in zone_entities:
        zone_dto = ZoneResponseDTO(
            id=zone.id,
            zone_number=zone.zone_number,
            is_active=zone.is_active,
            factory=FactoryDTO(
                name=zone.factory.name,
                abbr_name=zone.factory.abbr_name,
            ),
            created_at=zone.created_at,
            updated_at=zone.updated_at,
            levels=zone_level_map.get(zone.id, []),
        )
        zones.append(zone_dto)

    # Bước 3: Gói vào PaginateDTO
    paginate_schema = PaginateDTO(
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
        items=zones,
    )

    return Response.success_response(
        code="ETB-lay_danh_sach_thanh_cong",
        data=paginate_schema,
    ).get_dict()


# create zone
@router.post("/")
async def create_zone(
    token: TokenVerifyDep,
    body: CreateZoneSchema,
    use_case: CreateZoneUseCaseDep,
):
    zone_dto = ZoneDTO(
        zone_number=body.zone_number,
        factory=FactoryDTO(
            id=body.factory_id,
        ),
    )

    use_case.execute(zone_dto=zone_dto)

    return Response.success_response(
        code="ETB-tao_thanh_cong", data="Success"
    ).get_dict()


# update zone
@router.patch("/{zone_id}")
async def update_zone(
    token: TokenVerifyDep,
    zone_id: int,
    body: UpdateZoneSchema,
    use_case: UpdateZoneUseCaseDep,
):
    zone_dto = ZoneDTO(id=zone_id, zone_number=body.zone_number)

    use_case.execute(zone_dto=zone_dto)

    return Response.success_response(
        code="ETB-cap_nhat_thanh_cong", data="Success"
    ).get_dict()


# update status zone
@router.patch("/{zone_id}/status")
async def update_status_zone(
    token: TokenVerifyDep,
    zone_id: int,
    body: UpdateStatusZoneSchema,
    use_case: UpdateStatusZoneUseCaseDep,
):
    zone_dto = ZoneDTO(id=zone_id, is_active=body.is_active)

    use_case.execute(zone_dto=zone_dto)

    return Response.success_response(
        code="ETB-cap_nhat_status_thanh_cong", data="Success"
    ).get_dict()


@router.patch("/zone-levels/{zone_level_id}/status")
async def update_status_zone_level(
    token: TokenVerifyDep,
    zone_level_id: int,
    body: UpdateStatusLevelZoneSchema,
    use_case: UpdateStatusZoneLevelUseCaseDep,
):
    zone_level_dto = ZoneLevelDTO(id=zone_level_id, is_active=body.is_active)

    use_case.execute(zone_level_dto=zone_level_dto)

    return Response.success_response(
        code="ETB-cap_nhat_status_thanh_cong", data="Success"
    ).get_dict()
