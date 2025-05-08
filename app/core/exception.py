from typing import Dict, List, Any, Union


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
            for field, error_msg in details.items():
                self.errors.append({"field": field, "code": error_code})
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
        error_code: str = "ETB-404",
        details: Union[Dict[str, Any], List[Dict[str, Any]]] = None,
    ):
        super().__init__(error_code=error_code, status_code=404, details=details)


class ValidationError(DomainError):
    """Validation error."""

    def __init__(
        self,
        error_code: str = "ETB-422",
        details: Union[Dict[str, Any], List[Dict[str, Any]]] = None,
    ):
        super().__init__(error_code=error_code, status_code=422, details=details)


class AuthenticationError(DomainError):
    """Authentication error."""

    def __init__(
        self,
        error_code: str = "ETB-401",
        details: Union[Dict[str, Any], List[Dict[str, Any]]] = None,
    ):
        super().__init__(error_code=error_code, status_code=401, details=details)


class AuthorizationError(DomainError):
    """Authorization error."""

    def __init__(
        self,
        error_code: str = "ETB-403",
        details: Union[Dict[str, Any], List[Dict[str, Any]]] = None,
    ):
        super().__init__(error_code=error_code, status_code=403, details=details)


class BusinessRuleError(DomainError):
    """Business rule violation error."""

    def __init__(
        self,
        error_code: str = "ETB-409",
        details: Union[Dict[str, Any], List[Dict[str, Any]]] = None,
    ):
        super().__init__(error_code=error_code, status_code=409, details=details)
