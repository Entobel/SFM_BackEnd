from fastapi import APIRouter, Depends
from app.application.schemas.shift_schemas import ShiftDTO
from app.presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from app.presentation.schemas.filter_dto import FilterDTO
from presentation.api.v1.dependencies.grow_dependencies import ListGrowingUCDep

router = APIRouter(prefix="/growings", tags=["growings"])


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
        )
