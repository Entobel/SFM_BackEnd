from typing import Optional
from pydantic import BaseModal, Field


class CreateGrowingSchema(BaseModal):
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
    is_active: Optional[bool] = None
    created_by: Optional[int] = None
