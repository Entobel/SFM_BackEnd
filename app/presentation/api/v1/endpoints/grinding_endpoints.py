from fastapi import APIRouter, Depends
from loguru import logger

from app.application.dto.antioxidant_type_dto import AntioxidantTypeDTO
from app.application.dto.factory_dto import FactoryDTO
from app.application.dto.grinding_dto import GrindingDTO
from app.application.dto.packing_type_dto import PackingTypeDTO
from app.application.dto.shift_dto import ShiftDTO
from app.application.dto.user_dto import UserDTO
from app.presentation.api.v1.dependencies.grinding_dependencies import CreateGrindingUseCaseDep, ListGrindingReportUseCaseDep
from app.presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from app.presentation.schemas.antioxidant_schema import AntioxidantTypeResponseSchema
from app.presentation.schemas.factory_schema import FactoryResponseSchema
from app.presentation.schemas.filter_schema import FilterSchema, PaginateDTO
from app.presentation.schemas.grinding_schema import CreateGrindingSchema, GrindingResponseSchema
from app.presentation.schemas.packing_type_schema import PackingTypeResponseSchema
from app.presentation.schemas.response import Response
from app.presentation.schemas.shift_schema import ShiftResponseSchema
from app.presentation.schemas.unit_schema import UnitResponseSchema
from app.presentation.schemas.user_schema import UserResponseSchema

router = APIRouter(prefix="/grindings", tags=["Grinding"])

# Get List Grinding


@router.get("/")
async def list_grinding_reports(
        token_verify_dep: TokenVerifyDep,
        use_case: ListGrindingReportUseCaseDep,
        filter_params: FilterSchema = Depends()):

    result = use_case.execute(
        page=filter_params.page,
        page_size=filter_params.page_size,
        search=filter_params.search,
        factory_id=filter_params.factory_id,
        start_date=filter_params.start_date,
        end_date=filter_params.end_date,
        report_status=filter_params.report_status,
        is_active=filter_params.is_active
    )

    [_grinding_reports, [grinding_pending_count, grinding_rejected_count]] = (
        result["items"]
    )

    grinding_reports = [
        GrindingResponseSchema(
            id=g.id,
            date_reported=g.date_reported,
            quantity=g.quantity,
            batch_grinding_information=g.batch_grinding_information,
            notes=g.notes,
            start_time=g.start_time,
            end_time=g.end_time,
            status=g.status,
            shift=ShiftResponseSchema(
                id=g.shift.id,
                name=g.shift.name,
            ) if g.shift else None,
            factory=FactoryResponseSchema(
                id=g.factory.id,
                name=g.factory.name,
            ) if g.factory else None,
            antioxidant_type=AntioxidantTypeResponseSchema(
                id=g.antioxidant_type.id,
                name=g.antioxidant_type.name,
            ) if g.antioxidant_type else None,
            packing_type=PackingTypeResponseSchema(
                id=g.packing_type.id,
                name=g.packing_type.name,
                quantity=g.packing_type.quantity,
                unit=UnitResponseSchema(
                    id=g.packing_type.unit.id,
                    symbol=g.packing_type.unit.symbol,
                ),
            ) if g.packing_type else None,
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
        for g in _grinding_reports
    ]

    paginate_schema = PaginateDTO(
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
        items=grinding_reports,
    )

    return Response.success_response(
        code="ETB-lay_danh_sach_grinding_report_thanh_cong",
        data={
            **paginate_schema.model_dump(),
            "counts": {
                "pending": grinding_pending_count,
                "rejected": grinding_rejected_count,
            },
        },
    ).get_dict()


# Create Grinding Report


@router.post("/")
async def create_grinding_report(token_verify_dep: TokenVerifyDep, body: CreateGrindingSchema, use_case: CreateGrindingUseCaseDep):
    logger.debug(f"Creating grinding report with body: {body.model_dump()}")
    grinding_dto = GrindingDTO(
        date_reported=body.date_reported,
        antioxidant_type=AntioxidantTypeDTO(
            id=body.antioxidant_type_id
        ),
        start_time=body.start_time,
        end_time=body.end_time,
        packing_type=PackingTypeDTO(id=body.packing_type_id),
        quantity=body.quantity,
        batch_grinding_information=body.batch_grinding_information,
        factory=FactoryDTO(
            id=body.factory_id
        ),
        notes=body.notes,
        shift=ShiftDTO(
            id=body.shift_id
        ),
        created_by=UserDTO(
            id=body.created_by
        )
    )

    use_case.execute(grinding_dto=grinding_dto)

    return Response.success_response(
        data="Success", code="ETB_tao_growing_report_thanh_cong"
    ).get_dict()
