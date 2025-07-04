from datetime import datetime
from typing import Optional
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, model_validator, ConfigDict

from app.application.dto.diet_dto import DietDTO
from app.application.dto.factory_dto import FactoryDTO
from app.application.dto.growing_zone_level_dto import GrowingZoneLevelDTO
from app.application.dto.operation_type_dto import OperationTypeDTO
from app.application.dto.product_type_dto import ProductTypeDTO
from app.application.dto.shift_dto import ShiftDTO
from app.application.dto.user_dto import UserDTO
from app.domain.entities.shift_entity import ShiftEntity
from app.presentation.schemas.diet_schema import DietResponseSchema
from app.presentation.schemas.factory_schema import FactoryResponseSchema
from app.presentation.schemas.growing_zone_level_schema import (
    GrowingZoneLevelResponseSchema,
)
from app.presentation.schemas.product_type_schema import (
    ProductTypeResponseSchema,
)
from app.presentation.schemas.operation_type_schema import OperationTypeResponseSchema
from app.presentation.schemas.shift_schema import ShiftResponseSchema
from app.presentation.schemas.user_schema import UserResponseSchema
from app.presentation.schemas.zone_schema import ZoneResponseSchema


class GrowingResponseSchema(BaseModel):
    id: Optional[int] = None
    date_produced: Optional[datetime] = None
    shift: Optional[ShiftResponseSchema] = None
    product_type: Optional[ProductTypeResponseSchema] = None
    operation_type: Optional[OperationTypeResponseSchema] = None
    diet: Optional[DietResponseSchema] = None
    factory: Optional[FactoryResponseSchema] = None
    zone: Optional[ZoneResponseSchema] = None
    number_crates: Optional[int] = None
    substrate_moisture: Optional[float] = None
    notes: Optional[str] = None
    status: Optional[int] = None

    assigned_zone_levels: Optional[list[GrowingZoneLevelResponseSchema]] = None

    created_by: Optional[UserResponseSchema] = None
    created_at: Optional[datetime] = None

    approved_by: Optional[UserResponseSchema] = None
    approved_at: Optional[datetime] = None
    rejected_by: Optional[UserResponseSchema] = None
    rejected_at: Optional[datetime] = None
    rejected_reason: Optional[str] = None

    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class CreateGrowingSchema(BaseModel):
    date_produced: Optional[str] = None
    shift_id: Optional[int] = None
    product_type_id: Optional[int] = None
    operation_type_id: Optional[int] = None
    diet_id: Optional[int] = None
    factory_id: Optional[int] = None
    number_crates: Optional[int] = None
    substrate_moisture: Optional[float] = None
    notes: Optional[str] = None
    status: Optional[int] = None
    created_by: Optional[int] = None
    zone_id: Optional[int] = None
    zone_level_ids: Optional[list[int]] = None

    @model_validator(mode="before")
    @classmethod
    def check_required_fields(cls, values: dict[str, any]):
        required_fields = {
            "date_produced": "ETB-thieu_truong_date_produced",
            "shift_id": "ETB-thieu_truong_shift_id",
            "operation_type_id": "ETB-thieu_truong_operation_type_id",
            "product_type_id": "ETB-thieu_truong_product_type_id",
            "diet_id": "ETB-thieu_truong_diet_id",
            "factory_id": "ETB-thieu_truong_factory_id",
            "number_crates": "ETB-thieu_truong_number_crates",
            "created_by": "ETB-thieu_truong_created_by",
            "zone_level_ids": "ETB-thieu_truong_zone_level_ids",
            "zone_id": "ETB-thieu_truong_zone_id",
        }

        errors = []
        for field, error_code in required_fields.items():
            if field not in values or values[field] is None:
                errors.append(
                    {
                        "loc": ("body", field),
                        "msg": error_code,
                        "type": "value_error.missing",
                    }
                )
        if errors:
            raise RequestValidationError(errors)

        return values


class ListGrowingSchema(BaseModel):
    id: Optional[int] = None
    date_produced: Optional[datetime] = None
    shift: Optional[ShiftDTO] = None
    product_type: Optional[ProductTypeDTO] = None
    operation_type: Optional[OperationTypeDTO] = None
    diet: Optional[DietDTO] = None
    factory: Optional[FactoryDTO] = None
    number_crates: Optional[int] = None
    substrate_moisture: Optional[float] = None
    notes: Optional[str] = None
    status: Optional[int] = None

    # Zone Level
    assigned_zone_levels: Optional[list[GrowingZoneLevelDTO]] = None

    is_active: Optional[bool] = None
    # Creator
    created_by: Optional[UserDTO] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    # Rejector
    rejected_by: Optional[UserDTO] = None
    rejected_at: Optional[datetime] = None
    rejected_reason: Optional[str] = None
    # Approver
    approved_by: Optional[UserDTO] = None
    approved_at: Optional[datetime] = None


class UpdateStatusGrowingSchema(BaseModel):
    status: Optional[int] = None
    rejected_at: Optional[str] = Field(default=None)
    rejected_by: Optional[int] = Field(default=None)
    rejected_reason: Optional[str] = Field(default=None)
    approved_at: Optional[str] = Field(default=None)
    approved_by: Optional[int] = Field(default=None)

    @model_validator(mode="before")
    @classmethod
    def check_required_fields(cls, values: dict[str, any]):
        required_fields = {
            "status": "ETB-thieu_truong_status",
        }

        errors = []
        for field, error_code in required_fields.items():
            if field not in values or values[field] is None:
                errors.append(
                    {
                        "loc": ("body", field),
                        "msg": error_code,
                        "type": "value_error.missing",
                    }
                )
        if errors:
            raise RequestValidationError(errors)

        return values


class UpdateGrowingSchema(BaseModel):
    shift_id: Optional[int] = None
    operation_type_id: Optional[int] = None
    product_type_id: Optional[int] = None
    diet_id: Optional[int] = None
    factory_id: Optional[int] = None
    substrate_moisture: Optional[float] = None
    number_crates: Optional[int] = None
    zone_id: Optional[int] = None
    old_zone_id: Optional[int] = None
    old_zone_level_ids: Optional[list[int]] = None
    zone_level_ids: Optional[list[int]] = None
    approved_by: Optional[int] = None
    approved_at: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[int] = None

    @model_validator(mode="before")
    @classmethod
    def check_required_fields(cls, values: dict[str, any]):
        required_fields = {
            "shift_id": "ETB-thieu_truong_shift_id",
            "operation_type_id": "ETB-thieu_truong_operation_type_id",
            "product_type_id": "ETB-thieu_truong_product_type_id",
            "diet_id": "ETB-thieu_truong_diet_id",
            "factory_id": "ETB-thieu_truong_factory_id",
            "substrate_moisture": "ETB-thieu_truong_substrate_moisture",
            "number_crates": "ETB-thieu_truong_number_crates",
            "zone_id": "ETB-thieu_truong_zone_id",
            "old_zone_level_ids": "ETB-thieu_truong_old_zone_level_ids",
            "zone_level_ids": "ETB-thieu_truong_zone_level_ids",
            "approved_by": "ETB-thieu_truong_approved_by",
            "approved_at": "ETB-thieu_truong_approved_at",
            "status": "ETB-thieu_truong_status",
        }

        errors = []
        for field, error_code in required_fields.items():
            if field not in values or values[field] is None:
                errors.append(
                    {
                        "loc": ("body", field),
                        "msg": error_code,
                        "type": "value_error.missing",
                    }
                )
        if errors:
            raise RequestValidationError(errors)

        return values
