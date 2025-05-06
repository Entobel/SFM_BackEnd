from typing import List, Dict
from pydantic_settings import BaseSettings


class Configs(BaseSettings):
    # Base
    ENV: str = "dev"
    API: str = "/api"
    API_V1: str = "/api/v1"
    PROJECT_NAME: str = "sfm-api"
    DEBUG: bool = True

    DB_ENGINE_MAPPER: Dict[str, str] = {
        "postgresql": "postgresql",
    }

    # auth
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # database
    DB: str = "postgresql"
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str = "3306"

    @property
    def db_engine(self) -> str:
        return self.DB_ENGINE_MAPPER.get(self.DB, "postgresql")

    @property
    def db_name(self) -> str:
        return self.ENV_DATABASE_MAPPER.get(self.ENV, "dev-fca")

    @property
    def database_uri(self) -> str:
        return f"{self.db_engine}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.db_name}"

    PAGE: int = 1
    PAGE_SIZE: int = 20
    ORDERING: str = "-id"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


config = Configs()
