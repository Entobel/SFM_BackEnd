import logging
from fastapi import FastAPI, status
from starlette.middleware.cors import CORSMiddleware
from fastapi_socketio import SocketManager
from app.core.config import config
from app.core.database import db
from app.core.error import setup_error_handlers
from app.presentation.api.v1.routes import routers as v1_routers

# Configure logging
from loguru import logger


class AppCreator:
    def __init__(self):
        logger.info(
            f"[APP]:: Initializing application in {config.ENV} environment")

        self.app = FastAPI(
            title=config.PROJECT_NAME,
            description="",
            version=config.PROJECT_VERSION,
            docs_url="/documentation",
            openapi_tags=[
                {
                    "name": "Authentication",
                    "description": "Endpoints for login, logout, and token management",
                },
                {"name": "Users", "description": "User profile and account management"},
                {
                    "name": "Role",
                    "description": "Endpoints for managing user roles, including creation, updating, deletion, and role assignment.",
                },
                {"name": "default", "description": "Service health check"},
                {
                    "name": "Department",
                    "description": "Endpoints for managing departments",
                },
                {"name": "Factory", "description": "Endpoints for managing factories"},
                {"name": "Diet", "description": "Endpoints for managing diets"},
                {"name": "Shift", "description": "Endpoints for managing shifts"},
                {
                    "name": "Operation Type",
                    "description": "Endpoints for managing production types",
                },
                {
                    "name": "Production Object",
                    "description": "Endpoints for managing production objects",
                },
                {
                    "name": "Growing",
                    "description": "Endpoints for managing growings",
                },
            ],
            # Đặt exclude_none=True mặc định cho toàn bộ ứng dụng
            response_model_exclude_none=True,
        )

        # Ensure DB connection works
        if not db.test_connection():
            logger.error("Failed to connect to the database")
            raise RuntimeError("❌ Failed to connect to the database.")

        # Configure CORS middleware if applicable
        if config.BACKEND_CORS_ORIGINS:
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=[str(origin)
                               for origin in config.BACKEND_CORS_ORIGINS],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

            logger.success(
                f"CORS configured with origins: {config.BACKEND_CORS_ORIGINS}"
            )

        # Health check endpoint
        @self.app.get("/", status_code=status.HTTP_200_OK)
        async def health_check():
            return {"message": "Service is working on port 8000"}

        # Mount API v1 routes
        self.app.include_router(v1_routers, prefix=config.API_V1)
        logger.success(f"[APP]:: API routes mounted at {config.API_V1}")

        # Setup centralized error handling
        setup_error_handlers(self.app)
        logger.success("[APP]:: Centralized error handlers configured")


app_creator = AppCreator()
app = app_creator.app


# Log application startup
