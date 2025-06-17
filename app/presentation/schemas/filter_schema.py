from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field


class FilterSchema(BaseModel):
    """
    Reusable filter DTO for pagination and common filters.
    This can be used in multiple endpoints that require similar filtering parameters.
    """

    page: int = Field(default=1, description="Page number")
    page_size: int = Field(default=10, description="Number of items per page")
    search: str = Field(default="", description="Search query string")
    zone_id: Optional[int] = Field(
        default=None, description="Filter by zone ID")
    department_id: Optional[int] = Field(
        default=None, description="Filter by department ID"
    )
    factory_id: Optional[int] = Field(
        default=None, description="Filter by factory ID")
    role_id: Optional[int] = Field(
        default=None, description="Filter by role ID")
    is_active: Optional[bool] = Field(
        default=None, description="Filter by is active")
    operation_type_id: Optional[int] = Field(
        default=None, description="Filter by production type ID"
    )
    product_type_id: Optional[int] = Field(
        default=None, description="Filter by production object ID"
    )
    start_date: Optional[str] = Field(
        default=None, description="Filter by start date")
    end_date: Optional[str] = Field(
        default=None, description="Filter by end date")
    diet_id: Optional[int] = Field(
        default=None, description="Filter by diet ID")
    shift_id: Optional[int] = Field(
        default=None, description="Filter by shift ID")
    substrate_moisture_lower_bound: Optional[float] = Field(
        default=None, description="Filter by start range moisture ID"
    )
    zone_level_status: Optional[int] = Field(
        default=0, description="Filter by zone level status"
    )
    substrate_moisture_upper_bound: Optional[float] = Field(
        default=None, description="Filter by end range moisture ID"
    )
    report_status: Optional[int] = Field(
        default=None, description="Filter by status of report"
    )
    growing_zone_status: Optional[int] = Field(
        default=None, description="Filter by status of growing zone"
    )
    model_config = ConfigDict(from_attributes=True)


T = TypeVar("T")


class PaginateDTO(BaseModel, Generic[T]):
    total: int
    page: int
    page_size: int
    total_pages: int
    items: list[T]
