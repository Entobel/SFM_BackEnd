# presentation/schemas/response.py

from typing import Generic, TypeVar, Optional, List, Any, Dict
from pydantic import BaseModel, model_validator, ConfigDict

T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    success: bool
    code: Optional[str] = None
    data: Optional[T] = None
    errors: Optional[List[dict[str, str]]] = None

    model_config = ConfigDict(exclude_none=True)

    @model_validator(mode="after")
    def validate_fields(self) -> "Response":
        if self.success:
            # Success response should not have errors
            self.errors = None
        else:
            # Error response should not have data and code
            self.data = None
            self.code = None
        return self

    def get_dict(self) -> Dict[str, Any]:
        """
        Create a clean dictionary with only non-None fields.
        This ensures no null fields are included in the JSON response.
        """
        result = {"success": self.success}

        if self.success:
            if self.code is not None:
                result["code"] = self.code
            if self.data is not None:
                result["data"] = self.data
        else:
            if self.errors is not None:
                result["errors"] = self.errors

        return result

    @classmethod
    def success_response(cls, data: T, code: str = "Success") -> "Response[T]":
        return cls(success=True, code=code, data=data)

    @classmethod
    def error_response(cls, errors: List[dict[str, str]]) -> "Response":
        return cls(success=False, errors=errors)
