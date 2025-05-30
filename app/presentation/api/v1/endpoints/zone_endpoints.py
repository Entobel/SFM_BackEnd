from fastapi import APIRouter, Depends

from application.dto.zone_dto import ZoneDTO
from presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from presentation.api.v1.dependencies.zone_dependencies import (
    CreateZoneUseCaseDep, GetListZoneUseCaseDep, UpdateStatusZoneUseCaseDep,
    UpdateZoneUseCaseDep)
from presentation.schemas.filter_schema import FilterSchema, PaginateSchema
from presentation.schemas.response import Response
from presentation.schemas.zone_schema import (CreateZoneSchema,
                                              UpdateStatusZoneSchema,
                                              UpdateZoneSchema,
                                              ZoneResponseSchema)

router = APIRouter(prefix="/zones", tags=["Zones"])


# get list zone
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
    )
    zones = []

    for zone in result["items"]:
        zone_dto = ZoneResponseSchema(
            id=zone.id,
            zone_number=zone.zone_number,
            is_active=zone.is_active,
        )

        zones.append(zone_dto)

    paginate_schema = PaginateSchema(
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
        items=zones,
    )

    return Response.success_response(
        code="ETB-lay_danh_sach_thanh_cong", data=paginate_schema
    ).get_dict()


# create zone
@router.post("/")
async def create_zone(
    token: TokenVerifyDep,
    body: CreateZoneSchema,
    use_case: CreateZoneUseCaseDep,
):
    zone_dto = ZoneDTO(zone_number=body.zone_number)

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
