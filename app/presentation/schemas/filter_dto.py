from typing import Generic, Optional, TypeVar
from pydantic import BaseModel, ConfigDict, Field


class FilterDTO(BaseModel):
    """
    Reusable filter DTO for pagination and common filters.
    This can be used in multiple endpoints that require similar filtering parameters.
    """

    page: int = Field(default=1, description="Page number")
    page_size: int = Field(default=10, description="Number of items per page")
    search: str = Field(default="", description="Search query string")
    department_id: Optional[int] = Field(
        default=None, description="Filter by department ID"
    )
    factory_id: Optional[int] = Field(default=None, description="Filter by factory ID")
    role_id: Optional[int] = Field(default=None, description="Filter by role ID")
    is_active: Optional[bool] = Field(default=None, description="Filter by is active")
    production_type_id: Optional[int] = Field(
        default=None, description="Filter by production type ID"
    )
    production_object_id: Optional[int] = Field(
        default=None, description="Filter by production object ID"
    )
    diet_id: Optional[int] = Field(default=None, description="Filter by diet ID")
    shift_id: Optional[int] = Field(default=None, description="Filter by shift ID")
    model_config = ConfigDict(from_attributes=True)


T = TypeVar("T")


class PaginateDTO(BaseModel, Generic[T]):
    total: int
    page: int
    page_size: int
    total_pages: int
    items: list[T]
