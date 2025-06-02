from fastapi import APIRouter, Depends

from app.application.dto.level_dto import LevelDTO
from app.presentation.api.v1.dependencies.level_dependencies import (
    GetListLevelUCDep,
    CreateLevelUCDep,
    UpdateStatusLevelUCDep,
)
from app.presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from app.presentation.schemas.filter_schema import FilterSchema, PaginateDTO
from app.presentation.schemas.level_schema import (
    CreateLevelSchema,
    UpdateStatusLevelSchema,
)
from app.presentation.schemas.response import Response

router = APIRouter(prefix="/levels", tags=["Levels"])


@router.get("/")
async def get_list_levels(
    token: TokenVerifyDep,
    use_case: GetListLevelUCDep,
    filter_params: FilterSchema = Depends(),
):
    result = use_case.execute(
        page=filter_params.page,
        page_size=filter_params.page_size,
        search=filter_params.search,
        is_active=filter_params.is_active,
    )

    levels = []

    for level in result["items"]:
        level_dto = LevelDTO(
            id=level.id,
            name=level.name,
            is_active=level.is_active,
            created_at=level.created_at,
            updated_at=level.updated_at,
        )

        levels.append(level_dto)

    paginate_schema = PaginateDTO(
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
        items=levels,
    )

    return Response.success_response(
        code="ETB-lay_danh_sach_level_thanh_cong", data=paginate_schema
    ).get_dict()


@router.post("/")
async def create_level(
    token: TokenVerifyDep, use_case: CreateLevelUCDep, body: CreateLevelSchema
):
    level_dto = LevelDTO(
        name=body.name,
    )

    use_case.execute(level_dto=level_dto)

    return Response.success_response(
        code="ETB-tao_moi_level_thanh_cong", data="Success"
    ).get_dict()


# update status level
@router.patch("/{level_id}/status")
async def update_status_level(
    token: TokenVerifyDep,
    level_id: int,
    body: UpdateStatusLevelSchema,
    use_case: UpdateStatusLevelUCDep,
):
    level_dto = LevelDTO(id=level_id, is_active=body.is_active)

    use_case.execute(level_dto=level_dto)

    return Response.success_response(
        code="ETB-cap_nhat_status_level_thanh_cong", data="Success"
    ).get_dict()
