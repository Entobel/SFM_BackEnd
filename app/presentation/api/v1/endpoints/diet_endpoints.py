from application.schemas.diet_dto import DietDTO
from fastapi import APIRouter, Depends
from presentation.api.v1.dependencies.diet_dependencies import (
    CreateDietUCDep,
    ListDietUCDep,
    UpdateDietStatusUCDep,
    UpdateDietUCDep,
)
from presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from presentation.schemas.diet_dto import (
    CreateDietDTO,
    UpdateDietDTO,
    UpdateStatusDietDTO,
)
from presentation.schemas.filter_dto import FilterDTO, PaginateDTO
from presentation.schemas.response import Response

router = APIRouter(prefix="/diets", tags=["Diet"])


# List Diet
@router.get("/")
async def list_diets(
    token: TokenVerifyDep,
    use_case: ListDietUCDep,
    filter_params: FilterDTO = Depends(),
):
    result = use_case.execute(
        page=filter_params.page,
        page_size=filter_params.page_size,
        search=filter_params.search,
        is_active=filter_params.is_active,
    )

    diets = []

    for diet in result["items"]:
        diet_dto = DietDTO(
            id=diet.id,
            name=diet.name,
            description=diet.description,
            is_active=diet.is_active,
        )

        diets.append(diet_dto)

    paginate_data = PaginateDTO(
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
        items=diets,
    )

    return Response.success_response(
        code="ETB-lay_danh_sach_phong_ban_thanh_cong", data=paginate_data
    ).get_dict()


# Create Diet
@router.post("/")
async def create_diet(
    token: TokenVerifyDep,
    use_case: CreateDietUCDep,
    create_diet_dto: CreateDietDTO,
):
    diet_dto = DietDTO(
        name=create_diet_dto.name,
        description=create_diet_dto.description,
    )

    use_case.execute(diet_dto=diet_dto)

    return Response.success_response(
        code="ETB-tao_diet_thanh_cong", data="Success"
    ).get_dict()


# update diet status
@router.patch("/{diet_id}/status")
async def update_diet_status(
    token: TokenVerifyDep,
    diet_id: int,
    body: UpdateStatusDietDTO,
    use_case: UpdateDietStatusUCDep,
):
    diet_dto = DietDTO(
        id=diet_id,
        is_active=body.is_active,
    )
    use_case.execute(diet_dto=diet_dto)

    return Response.success_response(
        code="ETB-cap_nhat_trang_thai_di_thanh_cong", data="Success"
    ).get_dict()


@router.put("/{diet_id}")
async def update_diet(
    token: TokenVerifyDep,
    diet_id: int,
    body: UpdateDietDTO,
    use_case: UpdateDietUCDep,
):
    diet_dto = DietDTO(
        id=diet_id,
        name=body.name,
        description=body.description,
    )

    use_case.execute(diet_dto=diet_dto)

    return Response.success_response(
        code="ETB-cap_nhat_di_thanh_cong", data="Success"
    ).get_dict()
