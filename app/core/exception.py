from typing import Any, Dict, List, Union


class DomainError(Exception):
    """Base class for domain errors."""

    def __init__(
        self,
        error_code: str = "ETB-001",
        status_code: int = 400,
        details: Union[Dict[str, Any], List[Dict[str, Any]]] = None,
    ):
        super().__init__(error_code)
        self.status_code = status_code
        self.error_code = error_code

        # Convert details to the new list format if it's a dict
        if isinstance(details, dict):
            self.details = details  # Keep the original dict for backward compatibility
            self.errors = []
            for field, code in details.items():
                self.errors.append({"field": field, "code": code})
        elif isinstance(details, list):
            self.errors = []
            # Create a dict version for backward compatibility
            self.details = {}
            for error in details:
                if "field" in error:
                    field = error["field"]
                    error_code_to_use = error.get("code", error_code)
                    self.errors.append({"field": field, "code": error_code_to_use})
                    self.details[field] = error_code_to_use
        else:
            self.details = {}
            # Ensure there's always at least one error in the array with the error code
            self.errors = [{"code": error_code}]


class NotFoundError(DomainError):
    """Resource not found error."""

    def __init__(
        self,
        error_code: str = "ETB-khong_tim_thay_tai_nguyen",
        details: Union[Dict[str, Any], List[Dict[str, Any]]] = None,
    ):
        super().__init__(error_code=error_code, status_code=400, details=details)


class ValidationError(DomainError):
    """Validation error."""

    def __init__(
        self,
        error_code: str = "ETB-loi_du_lieu",
        details: Union[Dict[str, Any], List[Dict[str, Any]]] = None,
    ):
        super().__init__(error_code=error_code, status_code=400, details=details)


class AuthenticationError(DomainError):
    """Authentication error."""

    def __init__(
        self,
        error_code: str = "ETB-loi_xac_thuc",
        details: Union[Dict[str, Any], List[Dict[str, Any]]] = None,
    ):
        super().__init__(error_code=error_code, status_code=400, details=details)


class BadRequestError(DomainError):
    """Authentication error."""

    def __init__(
        self,
        error_code: str = "ETB-loi_yeu_cau",
        details: Union[Dict[str, Any], List[Dict[str, Any]]] = None,
    ):
        super().__init__(error_code=error_code, status_code=400, details=details)


class AuthorizationError(DomainError):
    """Authorization error."""

    def __init__(
        self,
        error_code: str = "ETB-khong_co_quyen_truy_cap",
        details: Union[Dict[str, Any], List[Dict[str, Any]]] = None,
    ):
        super().__init__(error_code=error_code, status_code=400, details=details)


class BusinessRuleError(DomainError):
    """Business rule violation error."""

    def __init__(
        self,
        error_code: str = "ETB-409",
        details: Union[Dict[str, Any], List[Dict[str, Any]]] = None,
    ):
        super().__init__(error_code=error_code, status_code=400, details=details)


class ForbiddenError(DomainError):
    """Business rule violation error."""

    def __init__(
        self,
        error_code: str = "ETB-403",
        details: Union[Dict[str, Any], List[Dict[str, Any]]] = None,
    ):
        super().__init__(error_code=error_code, status_code=400, details=details)
