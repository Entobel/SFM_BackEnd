from functools import wraps
from typing import Callable, Dict, Any, Type, List
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
import logging
import traceback

from .exception import DomainError
from presentation.schemas.response import Response

logger = logging.getLogger("app.error")


# -------------------- RESPONSE FORMATTER --------------------


def error_response(
    status_code: int, error_code: str = None, details: Dict | List = None
) -> Dict[str, Any]:
    """Format consistent error response."""
    errors = []
    code = error_code or f"ETB-{status_code}"

    if status_code == status.HTTP_422_UNPROCESSABLE_ENTITY and details:
        if isinstance(details, dict):
            for field in details.keys():
                errors.append({"field": field, "code": code})
        elif isinstance(details, list):
            for error in details:
                if isinstance(error, dict):
                    field = error.get("field")
                    if field:
                        errors.append({"field": field, "code": error.get("code", code)})
    else:
        errors.append({"code": code})

    return Response.error(errors)


# -------------------- DECORATOR FOR DOMAIN-SAFE HANDLING --------------------


def handler(func):
    """Error handler decorator for service functions."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DomainError as e:
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


# -------------------- CUSTOM EXCEPTION --------------------


class HTTPException(Exception):
    """Custom HTTP exception with formatted details."""

    def __init__(self, status_code: int, detail: Dict | str = None):
        self.status_code = status_code
        if isinstance(detail, str) or detail is None:
            self.detail = Response.error([{"code": f"ETB-{status_code}"}])
        else:
            self.detail = detail


# -------------------- ERROR HANDLER SETUP --------------------


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
        errors = []
        for err in exc.errors():
            loc = err.get("loc", [])
            if loc and loc[0] in {"body", "query", "path"}:
                loc = loc[1:]
            field = ".".join(str(part) for part in loc)

            msg = err.get("msg", "")

            # Cố gắng bóc code từ chuỗi "Value error, ETB-322"
            if isinstance(msg, str) and "ETB-" in msg:
                code = msg.split("ETB-")[-1]
                errors.append({"field": field, "code": f"ETB-{code.strip()}"})
            else:
                errors.append({"field": field, "code": "ETB-422"})

        return JSONResponse(status_code=422, content=Response.error(errors))

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        """Handle any unhandled exceptions."""
        logger.error(f"Unhandled exception: {str(exc)}")
        logger.error(traceback.format_exc())

        response = Response.error([{"code": "ETB-500"}])

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=response
        )
