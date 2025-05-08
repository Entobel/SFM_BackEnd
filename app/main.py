from fastapi import FastAPI, status
from api.v1.routes import routers as v1_routers
from core.config import config
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from core.database import db
from core.error import setup_error_handlers
import logging

# Configure logging
logger = logging.getLogger("uvicorn")


class AppCreator:
    def __init__(self):
        logger.info(f"[APP]:: Initializing application in {config.ENV} environment")

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
                    "name": "Roles",
                    "description": "Endpoints for managing user roles, including creation, updating, deletion, and role assignment.",
                },
            ],
        )

        if not db.test_connection():
            logger.error("[APP]:: Failed to connect to the database")
            raise RuntimeError("❌ Failed to connect to the database.")

        if config.BACKEND_CORS_ORIGINS:
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=[str(origin) for origin in config.BACKEND_CORS_ORIGINS],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
            logger.info(
                f"[APP]:: CORS configured with origins: {config.BACKEND_CORS_ORIGINS}"
            )

        # Check health route
        @self.app.get("/", status_code=status.HTTP_200_OK)
        async def health_check():
            return {"message": "Service is working"}

        # Include route
        self.app.include_router(v1_routers, prefix=config.API_V1)
        logger.info(f"[APP]:: API routes mounted at {config.API_V1}")

        # Setup centralized error handlers
        setup_error_handlers(self.app)
        logger.info("[APP]:: Centralized error handlers configured")


app_creator = AppCreator()
app = app_creator.app
