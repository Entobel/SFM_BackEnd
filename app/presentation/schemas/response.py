# presentation/schemas/response.py

from typing import Generic, TypeVar, Optional, List
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")


class Response(GenericModel, Generic[T]):
    success: bool
    code: Optional[str] = None
    data: Optional[T] = None

    @classmethod
    def success_response(cls, data: T, code: str = "Success") -> "Response[T]":
        return cls(success=True, code=code, data=data)

    @classmethod
    def error_response(cls, errors: List[dict[str, str]]) -> "Response":
        return cls(success=False, errors=errors)
