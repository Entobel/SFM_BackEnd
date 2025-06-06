import logging
from typing import Any, Callable, Dict, List, Type

import psycopg2
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from psycopg2 import errorcodes as pg_errorcodes
from app.presentation.schemas.response import Response
from app.core.exception import DomainError

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

    return Response.error_response(errors)


# -------------------- CUSTOM EXCEPTION --------------------


class HTTPException(Exception):
    """Custom HTTP exception with formatted details."""

    def __init__(self, status_code: int, detail: Dict | str = None):
        self.status_code = status_code
        if isinstance(detail, str) or detail is None:
            response = Response.error_response([{"code": f"ETB-{status_code}"}])
            self.detail = response.model_dump(exclude_none=True)
        else:
            self.detail = detail


# -------------------- ERROR HANDLER SETUP --------------------


def setup_error_handlers(app: FastAPI) -> None:
    """Configure global exception handlers for the FastAPI application."""

    # 1. Bắt hết DomainError (NotFoundError, ValidationError, v.v.)
    @app.exception_handler(DomainError)
    async def domain_error_handler(request: Request, exc: DomainError):
        # exc.errors đã được build sẵn trong DomainError
        response = Response.error_response(exc.errors)
        return JSONResponse(
            status_code=exc.status_code,
            content=response.model_dump(exclude_none=True),
        )

    # 2. Bắt validation lỗi của FastAPI (422)
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
            if isinstance(msg, str) and "ETB-" in msg:
                code = msg.split("ETB-")[-1]
                errors.append({"field": field, "code": f"ETB-{code.strip()}"})
            else:
                errors.append({"field": field, "code": "ETB-422"})
        response = Response.error_response(errors)
        return JSONResponse(
            status_code=422, content=response.model_dump(exclude_none=True)
        )

    # 3. Bắt mọi Exception chưa xử lý khác
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
        response = Response.error_response([{"code": "ETB-500"}])
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=response.model_dump(exclude_none=True),
        )

    @app.exception_handler(psycopg2.Error)
    async def psycopg2_exception_handler(request: Request, exc: psycopg2.Error):
        """
        Chuẩn hoá lỗi DB thành HTTP status + ETB-code quen thuộc.
        """
        sqlstate = exc.pgcode  # ví dụ '23505' = UNIQUE_VIOLATION
        mapping = {
            pg_errorcodes.UNIQUE_VIOLATION: status.HTTP_409_CONFLICT,
            pg_errorcodes.FOREIGN_KEY_VIOLATION: status.HTTP_409_CONFLICT,
            pg_errorcodes.NOT_NULL_VIOLATION: status.HTTP_400_BAD_REQUEST,
            pg_errorcodes.CHECK_VIOLATION: status.HTTP_400_BAD_REQUEST,
            pg_errorcodes.INVALID_TEXT_REPRESENTATION: status.HTTP_400_BAD_REQUEST,
        }
        status_code = mapping.get(sqlstate, status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Log chi tiết cho dev/ops
        logger.error(f"psycopg2 error {sqlstate or 'unknown'}: {exc}", exc_info=True)

        # Giữ nguyên convention ETB-<status>
        response = Response.error_response([{"code": f"ETB-{status_code}"}])
        return JSONResponse(
            status_code=status_code,
            content=response.model_dump(exclude_none=True),
        )
