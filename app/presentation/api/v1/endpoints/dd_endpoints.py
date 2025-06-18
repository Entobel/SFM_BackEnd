from fastapi import APIRouter, Depends
from loguru import logger

from app.application.dto.dd_dto import DdDTO
from app.application.dto.dried_larvae_discharge_type_dto import DriedLarvaeDischargeTypeDTO
from app.application.dto.dryer_machine_type_dto import DryerMachineTypeDTO
from app.application.dto.dryer_product_type_dto import DryerProductTypeDTO
from app.application.dto.factory_dto import FactoryDTO
from app.application.dto.shift_dto import ShiftDTO
from app.application.dto.user_dto import UserDTO
from app.presentation.api.v1.dependencies.dd_dependencies import CreateDdReportUseCaseDep, ListDdReportUseCaseDep
from app.presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from app.presentation.schemas.dd_schema import CreateDDSchema, DdResponseSchema
from app.presentation.schemas.dried_larvae_discharge_type_schema import DriedLarvaeDischargeTypeResponseSchema
from app.presentation.schemas.dryer_machine_type_schema import DryerMachineTypeResponseSchema
from app.presentation.schemas.dryer_product_type_schema import DryerProductTypeResponseSchema
from app.presentation.schemas.factory_schema import FactoryResponseSchema
from app.presentation.schemas.filter_schema import FilterSchema, PaginateDTO
from app.presentation.schemas.response import Response
from app.presentation.schemas.shift_schema import ShiftResponseSchema
from app.presentation.schemas.user_schema import UserResponseSchema


router = APIRouter(prefix="/dds", tags=["Drum Drying"])


@router.get('/')
async def list_dd_report(
        token_verify_dep: TokenVerifyDep,
        use_case: ListDdReportUseCaseDep,
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

    [_dd_reports, [dd_pending_count, dd_rejected_count]] = (
        result["items"]
    )

    dd_reports = [
        DdResponseSchema(
            id=dd.id,
            date_reported=dd.date_reported,
            quantity_fresh_larvae_input=dd.quantity_fresh_larvae_input,
            quantity_dried_larvae_output=dd.quantity_dried_larvae_output,
            temperature_after_2h=dd.temperature_after_2h,
            temperature_after_3h=dd.temperature_after_3h,
            temperature_after_3h30=dd.temperature_after_3h30,
            temperature_after_4h=dd.temperature_after_4h,
            temperature_after_4h30=dd.temperature_after_4h30,
            start_time=dd.start_time,
            end_time=dd.end_time,
            dried_larvae_moisture=dd.dried_larvae_moisture,
            drying_results=dd.drying_results,
            shift=ShiftResponseSchema(
                id=dd.shift.id,
                name=dd.shift.name if dd.shift else None
            ),
            factory=FactoryResponseSchema(
                id=dd.factory.id,
                name=dd.factory.name if dd.factory else None,
                abbr_name=dd.factory.abbr_name if dd.factory else None),
            dryer_machine_type=DryerMachineTypeResponseSchema(
                id=dd.dryer_machine_type.id,
                name=dd.dryer_machine_type.name if dd.dryer_machine_type else None,
                abbr_name=dd.dryer_machine_type.abbr_name if dd.dryer_machine_type else None
            ),
            dryer_product_type=DryerProductTypeResponseSchema(
                id=dd.dryer_product_type.id,
                name=dd.dryer_product_type.name if dd.dryer_product_type else None,
            ),
            dried_larvae_discharge_type=DriedLarvaeDischargeTypeResponseSchema(
                id=dd.dried_larvae_discharge_type.id,
                name=dd.dried_larvae_discharge_type.name if dd.dried_larvae_discharge_type else None
            ),
            notes=dd.notes,
            is_active=dd.is_active,
            status=dd.status,
            created_by=UserResponseSchema(
                id=dd.created_by.id,
                first_name=dd.created_by.first_name,
                last_name=dd.created_by.last_name,
                email=dd.created_by.email,
                phone=dd.created_by.phone,
            ),
            rejected_by=UserResponseSchema(
                id=dd.rejected_by.id,
                first_name=dd.rejected_by.first_name,
                last_name=dd.rejected_by.last_name,
                email=dd.rejected_by.email,
                phone=dd.rejected_by.phone,
            ),
            rejected_at=dd.rejected_at,
            rejected_reason=dd.rejected_reason,
            approved_by=UserResponseSchema(
                id=dd.approved_by.id,
                first_name=dd.approved_by.first_name,
                last_name=dd.approved_by.last_name,
                email=dd.approved_by.email,
                phone=dd.approved_by.phone,
            ),
            approved_at=dd.approved_at,
            created_at=dd.created_at,
            updated_at=dd.updated_at,
        ).model_dump(exclude_none=True)
        for dd in _dd_reports
    ]

    paginate_schema = PaginateDTO(
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
        items=dd_reports,
    )

    return Response.success_response(
        code="ETB-lay_danh_sach_dd_report_thanh_cong",
        data={
            **paginate_schema.model_dump(),
            "counts": {
                "pending": dd_pending_count,
                "rejected": dd_rejected_count,
            },
        },
    ).get_dict()


@router.post('/')
async def create_dd_report(token_verify_dep: TokenVerifyDep, body: CreateDDSchema, use_case: CreateDdReportUseCaseDep):
    dd_dto = DdDTO(
        date_reported=body.date_reported,
        shift=ShiftDTO(id=body.shift_id),
        dried_larvae_discharge_type=DriedLarvaeDischargeTypeDTO(
            id=body.dried_larvae_discharge_type_id
        ),
        created_by=UserDTO(
            id=body.created_by
        ),
        dryer_machine_type=DryerMachineTypeDTO(
            id=body.dryer_machine_type_id
        ),
        dryer_product_type=DryerProductTypeDTO(
            id=body.dryer_product_type_id
        ),
        drying_results=body.drying_results,
        start_time=body.start_time,
        end_time=body.end_time,
        dried_larvae_moisture=body.dried_larvae_moisture,
        factory=FactoryDTO(
            id=body.factory_id
        ),
        quantity_dried_larvae_output=body.quantity_dried_larvae_output,
        quantity_fresh_larvae_input=body.quantity_fresh_larvae_input,
        temperature_after_2h=body.temperature_after_2h,
        temperature_after_3h=body.temperature_after_3h,
        temperature_after_3h30=body.temperature_after_3h30,
        temperature_after_4h=body.temperature_after_4h,
        temperature_after_4h30=body.temperature_after_4h30,
        notes=body.notes,
    )

    use_case.execute(dd_dto=dd_dto)

    return Response.success_response(
        data="Success", code="ETB_tao_dd_report_thanh_cong"
    ).get_dict()
