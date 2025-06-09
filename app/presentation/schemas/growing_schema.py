from datetime import datetime
from typing import Optional
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, model_validator, ConfigDict

from app.application.dto.diet_dto import DietDTO
from app.application.dto.factory_dto import FactoryDTO
from app.application.dto.growing_zone_level_dto import GrowingZoneLevelDTO
from app.application.dto.produciton_type_dto import ProductionTypeDTO
from app.application.dto.production_object_dto import ProductionObjectDTO
from app.application.dto.shift_dto import ShiftDTO
from app.application.dto.user_dto import UserDTO
from app.domain.entities.shift_entity import ShiftEntity
from app.presentation.schemas.diet_schema import DietResponseSchema
from app.presentation.schemas.factory_schema import FactoryResponseSchema
from app.presentation.schemas.growing_zone_level_schema import (
    GrowingZoneLevelResponseSchema,
)
from app.presentation.schemas.production_object_schema import (
    ProductionObjectResponseSchema,
)
from app.presentation.schemas.production_type_schema import ProductionTypeResponseSchema
from app.presentation.schemas.shift_schema import ShiftResponseSchema
from app.presentation.schemas.user_schema import UserResponseSchema


class GrowingResponseSchema(BaseModel):
    id: Optional[int] = None
    date_produced: Optional[datetime] = None
    shift: Optional[ShiftResponseSchema] = None
    production_object: Optional[ProductionObjectResponseSchema] = None
    production_type: Optional[ProductionTypeResponseSchema] = None
    diet: Optional[DietResponseSchema] = None
    factory: Optional[FactoryResponseSchema] = None
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
    production_object_id: Optional[int] = None
    production_type_id: Optional[int] = None
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
            "production_type_id": "ETB-thieu_truong_production_type_id",
            "production_object_id": "ETB-thieu_truong_production_object_id",
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
    production_object: Optional[ProductionObjectDTO] = None
    production_type: Optional[ProductionTypeDTO] = None
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


class UpdateGrowingSchema(BaseModel):
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
