from fastapi import FastAPI, status
from apis.v1.routes import routers as v1_routers
from utils.config import config
from starlette.middleware.cors import CORSMiddleware
from utils.class_object import singleton


@singleton
class AppCreator:
    def __init__(self):
        self.app = FastAPI(
            title=config.PROJECT_NAME,
            description="",
        )

        if config.BACKEND_CORS_ORIGINS:
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=[str(origin) for origin in config.BACKEND_CORS_ORIGINS],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

        # Check health route
        @self.app.get("/", status_code=status.HTTP_200_OK)
        async def root():
            return {"message": "Service is working"}

        # Include route
        self.app.include_router(v1_routers, prefix=config.API_V1)


app_creator = AppCreator()
app = app_creator.app
