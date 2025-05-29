from application.schemas.factory_dto import FactoryDTO
from domain.entities.factory_entity import FactoryEntity
from fastapi import APIRouter, Depends
from presentation.api.v1.dependencies.factory_dependencies import (
    CreateFactoryUseCaseDep,
    ListFactoryUseCaseDep,
    UpdateFactoryUseCaseDep,
    UpdateStatusFactoryUseCaseDep,
)
from presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from presentation.schemas.factory_dto import (
    CreateFactoryDTO,
    UpdateFactoryDTO,
    UpdateStatusFactoryDTO,
)
from presentation.schemas.filter_dto import FilterDTO, PaginateDTO
from presentation.schemas.response import Response

router = APIRouter(prefix="/factories", tags=["Factory"])


@router.get("/", response_model_exclude_none=True)
async def get_list_factory(
    token: TokenVerifyDep,
    use_case: ListFactoryUseCaseDep,
    filter_params: FilterDTO = Depends(),
):
    result = use_case.execute(
        page=filter_params.page,
        page_size=filter_params.page_size,
        search=filter_params.search,
        is_active=filter_params.is_active,
    )

    factories = []

    for factory in result["items"]:
        factory_dto = FactoryDTO(
            id=factory.id,
            name=factory.name,
            abbr_name=factory.abbr_name,
            description=factory.description,
            location=factory.location,
            is_active=factory.is_active,
        )
        factories.append(factory_dto)

    paginate_data = PaginateDTO(
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
        items=factories,
    )

    return Response.success_response(
        code="ETB-lay_danh_sach_nha_may_thanh_cong", data=paginate_data
    ).get_dict()


@router.post("/", response_model_exclude_none=True)
async def create_factory(
    token: TokenVerifyDep,
    factory_dto: CreateFactoryDTO,
    use_case: CreateFactoryUseCaseDep,
):
    factory = FactoryEntity(
        name=factory_dto.name,
        abbr_name=factory_dto.abbr_name,
        description=factory_dto.description,
        location=factory_dto.location,
    )

    use_case.execute(factory=factory)

    return Response.success_response(
        code="ETB-tao_nha_may_thanh_cong", data="Success"
    ).get_dict()


@router.put("/{factory_id}", response_model_exclude_none=True)
async def update_factory(
    token: TokenVerifyDep,
    factory_id: int,
    body: UpdateFactoryDTO,
    use_case: UpdateFactoryUseCaseDep,
):

    use_case.execute(
        factory_id=factory_id,
        factory_dto=FactoryDTO(
            name=body.name,
            abbr_name=body.abbr_name,
            description=body.description,
            location=body.location,
        ),
    )

    return Response.success_response(
        code="ETB-cap_nhat_nha_may_thanh_cong", data="Success"
    ).get_dict()


@router.patch("/{factory_id}/status", response_model_exclude_none=True)
async def update_factory_status(
    token: TokenVerifyDep,
    factory_id: int,
    body: UpdateStatusFactoryDTO,
    use_case: UpdateStatusFactoryUseCaseDep,
):
    use_case.execute(
        factory_id=factory_id,
        is_active=body.is_active,
    )

    return Response.success_response(
        code="ETB-cap_nhat_trang_thai_nha_may_thanh_cong", data="Success"
    ).get_dict()
