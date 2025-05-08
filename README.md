# Centralized Error Handling with I18n Support

This document provides guidelines for using the centralized error handling system with internationalization (i18n) support.

## Overview

The error handling system follows clean architecture principles by:

1. Defining domain-specific exceptions that represent business errors
2. Providing a centralized way to handle and format error responses
3. Using error codes instead of messages for client-side internationalization
4. Ensuring consistent error response structure across the application
5. Separating error handling concerns from business logic

## Error Response Structure

The error response format differs slightly based on the error type:

### Validation Errors (422)

For validation errors (status code 422), the format includes field information:

```json
{
	"success": false,
	"errors": [
		{
			"field": "username",
			"code": "ETB-422"
		},
		{
			"field": "email",
			"code": "ETB-422"
		}
	]
}
```

### Other Errors (400, 401, 403, 404, 409, 500, etc.)

For non-validation errors, the format uses a simpler structure:

```json
{
	"success": false,
	"errors": [
		{
			"code": "ETB-403"
		}
	]
}
```

## Exception Types

The system provides several specialized exception types:

-   `DomainError`: Base class for all domain-specific errors
-   `NotFoundError`: Resource not found (404)
-   `ValidationError`: Input validation failed (422)
-   `AuthenticationError`: Authentication failed (401)
-   `AuthorizationError`: User lacks permission (403)
-   `BusinessRuleError`: Business rule violation (409)

## How to Use

### 1. Use the Error Handler Decorator

Apply the `@handler` decorator to your use case methods to automatically catch and format exceptions:

```python
from core.error import handler

class MyUseCase:
    @handler
    def execute(self, data):
        # Your logic here
        pass
```

### 2. Raising Validation Errors (422)

When raising validation errors, provide field information:

```python
from core.exception import ValidationError

# Using list style with specific error codes
errors = [
    {"field": "email", "code": "ETB-EMAIL-INVALID"},
    {"field": "password", "code": "ETB-PASSWORD-SHORT"}
]

raise ValidationError(
    error_code="ETB-VALIDATION-422",  # Generic error code
    details=errors  # Field-specific errors
)

# OR using dictionary style (simpler but less flexible)
errors = {
    "email": "ETB-EMAIL-INVALID",
    "password": "ETB-PASSWORD-SHORT"
}

raise ValidationError(
    error_code="ETB-VALIDATION-422",  # This code will be used for all fields
    details=errors
)
```

### 3. Raising Other Error Types

For non-validation errors, you can simply raise the appropriate exception with an error code:

```python
from core.exception import NotFoundError

raise NotFoundError(
    error_code="ETB-USER-NOT-FOUND"  # Custom error code for i18n
)
```

### 4. Using Specific Error Codes

It's recommended to use specific, descriptive error codes for better i18n:

```python
# Instead of generic codes:
raise ValidationError(error_code="ETB-422")

# Use specific codes:
raise ValidationError(error_code="ETB-USERNAME-REQUIRED")
# or
raise ValidationError(
    error_code="ETB-VALIDATION",
    details=[{"field": "username", "code": "ETB-USERNAME-REQUIRED"}]
)
```

## Client-Side Internationalization

The system is designed to work with client-side internationalization:

1. The backend only provides error codes, not human-readable messages
2. The client uses these codes to look up appropriate translated messages
3. This allows changing languages without requiring backend changes
4. For validation errors, the field name is included to provide context

## Error Code Naming Conventions

Follow these conventions for error codes:

1. All error codes should start with the `ETB-` prefix
2. Use uppercase letters and hyphens for separating words
3. Include module or feature name in the error code
4. Be specific and descriptive

Examples:

-   `ETB-USER-NOT-FOUND`
-   `ETB-PERMISSION-DENIED`
-   `ETB-USERNAME-REQUIRED`
-   `ETB-EMAIL-INVALID`

## Example

See `app/application/examples/error_handling_example.py` for practical examples of how to use the error handling system in different scenarios.
