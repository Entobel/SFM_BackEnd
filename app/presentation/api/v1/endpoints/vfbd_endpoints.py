from fastapi import APIRouter, Depends
from loguru import logger

from app.application.dto.dried_larvae_discharge_type_dto import (
    DriedLarvaeDischargeTypeDTO,
)
from app.application.dto.dryer_product_type_dto import DryerProductTypeDTO
from app.application.dto.factory_dto import FactoryDTO
from app.application.dto.product_type_dto import ProductTypeDTO
from app.application.dto.shift_dto import ShiftDTO
from app.application.dto.user_dto import UserDTO
from app.application.dto.vfbd_dto import VfbdDTO
from app.presentation.api.v1.dependencies.user_dependencies import TokenVerifyDep
from app.presentation.api.v1.dependencies.vfbd_dependencies import (
    CreateVfbdReportUseCaseDep,
    ListVfbdReportUseCaseDep,
    UpdateVfbdReportUseCaseDep,
)
from app.presentation.schemas.dried_larvae_discharge_type_schema import (
    DriedLarvaeDischargeTypeResponseSchema,
)
from app.presentation.schemas.dryer_product_type_schema import (
    DryerProductTypeResponseSchema,
)
from app.presentation.schemas.factory_schema import FactoryResponseSchema
from app.presentation.schemas.filter_schema import FilterSchema, PaginateDTO
from app.presentation.schemas.response import Response
from app.presentation.schemas.shift_schema import ShiftResponseSchema
from app.presentation.schemas.user_schema import UserResponseSchema
from app.presentation.schemas.vfbd_schema import (
    CreateVFBDSchema,
    UpdateVFBDSchema,
    VfbdReponseSchema,
)


router = APIRouter(prefix="/vfbds", tags=["Vibratory Fluid Bed Drying"])


@router.get("/")
async def list_vfbd_report(
    token_verify_dep: TokenVerifyDep,
    use_case: ListVfbdReportUseCaseDep,
    filter_params: FilterSchema = Depends(),
):
    result = use_case.execute(
        page=filter_params.page,
        page_size=filter_params.page_size,
        search=filter_params.search,
        factory_id=filter_params.factory_id,
        start_date=filter_params.start_date,
        end_date=filter_params.end_date,
        report_status=filter_params.report_status,
        is_active=filter_params.is_active,
    )
    [_vfbd_reports, [vfbd_pending_count, vfbd_rejected_count]] = result["items"]

    vfbd_reports = [
        VfbdReponseSchema(
            id=vfbd.id,
            date_reported=vfbd.date_reported,
            dried_larvae_moisture=vfbd.dried_larvae_moisture,
            quantity_dried_larvae_sold=vfbd.quantity_dried_larvae_sold,
            drying_result=vfbd.drying_result,
            start_time=vfbd.start_time,
            end_time=vfbd.end_time,
            harvest_time=vfbd.harvest_time,
            temperature_output_1st=vfbd.temperature_output_1st,
            temperature_output_2nd=vfbd.temperature_output_2nd,
            shift=ShiftResponseSchema(
                id=vfbd.shift.id, name=vfbd.shift.name if vfbd.shift else None
            ),
            factory=FactoryResponseSchema(
                id=vfbd.factory.id,
                name=vfbd.factory.name if vfbd.factory else None,
                abbr_name=vfbd.factory.abbr_name if vfbd.factory else None,
            ),
            dryer_product_type=DryerProductTypeResponseSchema(
                id=vfbd.dryer_product_type.id,
                name=vfbd.dryer_product_type.name if vfbd.dryer_product_type else None,
            ),
            dried_larvae_discharge_type=DriedLarvaeDischargeTypeResponseSchema(
                id=vfbd.dried_larvae_discharge_type.id,
                name=(
                    vfbd.dried_larvae_discharge_type.name
                    if vfbd.dried_larvae_discharge_type
                    else None
                ),
            ),
            notes=vfbd.notes,
            is_active=vfbd.is_active,
            status=vfbd.status,
            created_by=UserResponseSchema(
                id=vfbd.created_by.id,
                first_name=vfbd.created_by.first_name,
                last_name=vfbd.created_by.last_name,
                email=vfbd.created_by.email,
                phone=vfbd.created_by.phone,
            ),
            rejected_by=UserResponseSchema(
                id=vfbd.rejected_by.id,
                first_name=vfbd.rejected_by.first_name,
                last_name=vfbd.rejected_by.last_name,
                email=vfbd.rejected_by.email,
                phone=vfbd.rejected_by.phone,
            ),
            rejected_at=vfbd.rejected_at,
            rejected_reason=vfbd.rejected_reason,
            approved_by=UserResponseSchema(
                id=vfbd.approved_by.id,
                first_name=vfbd.approved_by.first_name,
                last_name=vfbd.approved_by.last_name,
                email=vfbd.approved_by.email,
                phone=vfbd.approved_by.phone,
            ),
            approved_at=vfbd.approved_at,
            created_at=vfbd.created_at,
            updated_at=vfbd.updated_at,
        ).model_dump(exclude_none=True)
        for vfbd in _vfbd_reports
    ]

    paginate_schema = PaginateDTO(
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
        items=vfbd_reports,
    )

    return Response.success_response(
        code="ETB-lay_danh_sach_vfbd_report_thanh_cong",
        data={
            **paginate_schema.model_dump(),
            "counts": {
                "pending": vfbd_pending_count,
                "rejected": vfbd_rejected_count,
            },
        },
    ).get_dict()


@router.post("/")
async def create_vfbd_report(
    token_verify_def: TokenVerifyDep,
    body: CreateVFBDSchema,
    use_case: CreateVfbdReportUseCaseDep,
):

    vfbd_dto = VfbdDTO(
        date_reported=body.date_reported,
        shift=ShiftDTO(id=body.shift_id),
        factory=FactoryDTO(id=body.factory_id),
        start_time=body.start_time,
        end_time=body.end_time,
        harvest_time=body.harvest_time,
        temperature_output_1st=body.temperature_output_1st,
        temperature_output_2nd=body.temperature_output_2nd,
        dryer_product_type=DryerProductTypeDTO(id=body.dryer_product_type_id),
        dried_larvae_discharge_type=DriedLarvaeDischargeTypeDTO(
            id=body.dried_larvae_discharge_type_id
        ),
        quantity_dried_larvae_sold=body.quantity_dried_larvae_sold,
        dried_larvae_moisture=body.dried_larvae_moisture,
        drying_result=body.drying_result,
        notes=body.notes,
        created_by=UserDTO(id=body.created_by),
    )

    use_case.execute(vfbd_dto=vfbd_dto)

    return Response.success_response(
        data="Success", code="ETB_tao_vfbd_report_thanh_cong"
    ).get_dict()


@router.put("/{vfbd_id}")
async def update_vfbd_report(
    token_verify_def: TokenVerifyDep,
    vfbd_id: int,
    body: UpdateVFBDSchema,
    use_case: UpdateVfbdReportUseCaseDep,
):
    vfbd_dto = VfbdDTO(
        id=vfbd_id,
        shift=ShiftDTO(id=body.shift_id),
        factory=FactoryDTO(id=body.factory_id),
        start_time=body.start_time,
        end_time=body.end_time,
        harvest_time=body.harvest_time,
        temperature_output_1st=body.temperature_output_1st,
        temperature_output_2nd=body.temperature_output_2nd,
        dryer_product_type=DryerProductTypeDTO(id=body.dryer_product_type_id),
        dried_larvae_discharge_type=DriedLarvaeDischargeTypeDTO(
            id=body.dried_larvae_discharge_type_id
        ),
        quantity_dried_larvae_sold=body.quantity_dried_larvae_sold,
        dried_larvae_moisture=body.dried_larvae_moisture,
        drying_result=body.drying_result,
        notes=body.notes,
    )

    use_case.execute(vfbd_dto=vfbd_dto)

    return Response.success_response(
        data="Success", code="ETB_cap_nhat_vfbd_report_thanh_cong"
    ).get_dict()
