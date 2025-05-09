from functools import wraps
from typing import Callable, Dict, Any, Type, List
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from .exception import DomainError

from presentation.schemas.response import Response

import logging
import traceback

logger = logging.getLogger("app.error")


def error_response(
    status_code: int, error_code: str = None, details: Dict | List = None
) -> Dict[str, Any]:
    """Format consistent error response with i18n support."""
    errors = []
    code = error_code or f"ETB-{status_code}"

    # For 422 validation errors, include field name with code
    if status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
        if details:
            if isinstance(details, dict):
                for field, _ in details.items():
                    errors.append({"field": field, "code": code})
            elif isinstance(details, list):
                for error in details:
                    if isinstance(error, dict) and "field" in error:
                        errors.append(
                            {
                                "field": error.get("field", ""),
                                "code": error.get("code", code),
                            }
                        )
    # For other error types, just include code
    else:
        errors.append({"code": code})

    return Response.error(errors)


def handler(func):
    """Error handler decorator for service functions."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DomainError as e:

            # The response detail will only contain the success flag and errors list
            raise HTTPException(
                status_code=e.status_code,
                detail=Response.error(e.errors),
            )
        except Exception as e:
            logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=Response.error([{"code": "ETB-500"}]),
            )

    return wrapper


class HTTPException(Exception):
    """Custom HTTP exception with formatted details."""

    def __init__(self, status_code: int, detail: Dict | str):
        self.status_code = status_code
        if isinstance(detail, str):
            self.detail = Response.error([{"code": f"ETB-{status_code}"}])
        else:
            self.detail = detail


def setup_error_handlers(app: FastAPI) -> None:
    """Configure global exception handlers for the FastAPI application."""

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Handle custom HTTP exceptions."""
        return JSONResponse(status_code=exc.status_code, content=exc.detail)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        """Handle request validation errors."""
        logger.error(f"Validation error: {exc.errors()}")

        # Convert validation errors to format with field and code
        errors = []
        for error in exc.errors():
            loc = ".".join([str(x) for x in error.get("loc", [])])
            if loc:
                errors.append({"field": loc, "code": "ETB-422"})

        response = Response.error(errors)

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=response
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        """Handle any unhandled exceptions."""
        logger.error(f"Unhandled exception: {str(exc)}")
        logger.error(traceback.format_exc())

        response = Response.error([{"code": "ETB-500"}])

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=response
        )
