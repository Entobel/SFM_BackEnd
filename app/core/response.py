from typing import Generic, TypeVar, Dict, Any, Optional, List

T = TypeVar("T")  # Generic type for response data


class Response(Generic[T]):
    """Standard response format for API endpoints."""

    @staticmethod
    def success(data: T, message: str = "Success") -> Dict[str, Any]:
        """Create a standardized success response."""
        return {"success": True, "message": message, "data": data}

    @staticmethod
    def error(errors: List[Dict[str, str]], success: bool = False) -> Dict[str, Any]:
        """Create a standardized error response."""
        return {"success": success, "errors": errors}
