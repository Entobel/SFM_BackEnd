from fastapi import APIRouter, Depends
from presentation.schemas.response import Response
from application.schemas.diet_schemas import DietDTO
from application.schemas.user_schemas import UserDTO
from application.schemas.production_object_schemas import ProductionObjectDTO
from application.schemas.produciton_type_schemas import ProductionTypeDTO
from application.schemas.shift_schemas import ShiftDTO
from presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from presentation.schemas.filter_dto import FilterDTO, PaginateDTO
from presentation.schemas.growing_dto import CreateGrowingDTO, GrowingDTO
from presentation.api.v1.dependencies.growing_dependencies import (
    CreateGrowingUCDep,
    ListGrowingUCDep,
)

router = APIRouter(prefix="/growings", tags=["Growing"])


@router.get("/")
def list_growings(
    token: TokenVerifyDep,
    use_case: ListGrowingUCDep,
    filter: FilterDTO = Depends(),
):
    result = use_case.execute(
        page=filter.page,
        page_size=filter.page_size,
        search=filter.search,
        shift_id=filter.shift_id,
        start_date=filter.start_date,
        end_date=filter.end_date,
        production_type_id=filter.production_type_id,
        production_object_id=filter.production_object_id,
        diet_id=filter.diet_id,
    )

    growings = []

    for growing in result["items"]:
        growing_dto = GrowingDTO(
            id=growing.id,
            date_produced=growing.date_produced,
            shift=ShiftDTO(
                id=growing.shift.id,
                name=growing.shift.name,
                description=growing.shift.description,
            ),
            production_type=ProductionTypeDTO(
                id=growing.production_type.id,
                name=growing.production_type.name,
                description=growing.production_type.description,
            ),
            production_object=ProductionObjectDTO(
                id=growing.production_object.id,
                name=growing.production_object.name,
                description=growing.production_object.description,
            ),
            diet=DietDTO(
                id=growing.diet.id,
                name=growing.diet.name,
                description=growing.diet.description,
            ),
            user=UserDTO(
                id=growing.user.id,
                email=growing.user.email,
                phone=growing.user.phone,
                first_name=growing.user.first_name,
                last_name=growing.user.last_name,
            ),
            number_crates=growing.number_crates,
            substrate_moisture=growing.substrate_moisture,
            location_1=growing.location_1,
            location_2=growing.location_2,
            location_3=growing.location_3,
            location_4=growing.location_4,
            location_5=growing.location_5,
            notes=growing.notes,
        )
        growings.append(growing_dto)

    paginate_data = PaginateDTO(
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
        items=growings,
    )

    return Response.success_response(
        code="ETB-lay_danh_sach_thanh_cong", data=paginate_data
    ).get_dict()


@router.post("/", response_model_exclude_none=True)
def create_growing(
    token: TokenVerifyDep,
    body: CreateGrowingDTO,
    use_case: CreateGrowingUCDep,
):
    use_case.execute(body)

    return Response.success_response(
        code="ETB-tao_thanh_cong", data="Success"
    ).get_dict()
