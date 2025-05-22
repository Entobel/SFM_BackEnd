from fastapi import APIRouter, Depends

from presentation.schemas.response import Response
from application.schemas.diet_schemas import DietDTO
from presentation.schemas.filter_dto import FilterDTO, PaginateDTO
from presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from presentation.api.v1.dependencies.diet_dependencies import ListDietUCDep


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
