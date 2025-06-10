import logging
from typing import Dict, List, Optional

from dotenv import load_dotenv
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings
from loguru import logger

# Load environment variables from .env file
load_dotenv()


class DatabaseConfig(BaseSettings):
    """Database configuration settings."""

    DB: str = Field(..., description="Database type (e.g., postgresql)")
    DB_USER: str = Field(..., description="Database username")
    DB_PASSWORD: str = Field(..., description="Database password")
    DB_NAME: str = Field(..., description="Database name")
    DB_HOST: str = Field(..., description="Database host")
    DB_PORT: str = Field(default="5432", description="Database port")

    @property
    def database_uri(self) -> str:
        """Construct database URI from configuration."""
        return (
            f"{self.DB}://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @field_validator("DB")
    @classmethod
    def validate_db_type(cls, v: str) -> str:
        """Validate database type."""
        valid_types = ["postgresql", "mysql", "sqlite"]
        if v.lower() not in valid_types:
            raise ValueError(
                f"Invalid database type. Must be one of: {', '.join(valid_types)}"
            )
        return v.lower()

    model_config = {"extra": "allow"}


class SecurityConfig(BaseSettings):
    """Security-related configuration settings."""

    ALGORITHM: str = "HS256"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=60 * 24 * 30,  # 30 days
        description="Access token expiration time in minutes",
    )

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Validate secret key length."""
        if len(v) < 2:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v

    model_config = {"extra": "allow"}


class Configs(BaseSettings):
    """Main application configuration settings."""

    # Environment and API settings
    ENV: str = Field(default="dev", description="Environment (dev/prod)")
    API_V1: str = Field(default="/api/v1", description="API version 1 prefix")
    PROJECT_NAME: str = Field(
        default="Shopfloor Management", description="Project name"
    )
    PROJECT_VERSION: str = Field(default="0.0.1", description="Project version")
    DEBUG: bool = Field(default=True, description="Debug mode flag")

    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = Field(
        default=["*"], description="List of allowed CORS origins"
    )

    # Nested configurations
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)

    @property
    def database_uri(self) -> str:
        """Get database URI from nested configuration."""
        return self.database.database_uri

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.ENV.lower() == "prod"

    @field_validator("ENV")
    @classmethod
    def validate_env(cls, v: str) -> str:
        """Validate environment setting."""
        valid_envs = ["dev", "prod", "test"]
        if v.lower() not in valid_envs:
            raise ValueError(
                f"Invalid environment. Must be one of: {', '.join(valid_envs)}"
            )
        return v.lower()

    model_config = {
        "extra": "allow",
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "env_nested_delimiter": "__",
    }


# Initialize configuration
try:
    config = Configs()
    logger.info(f"Configuration loaded successfully for environment: {config.ENV}")
except Exception as e:
    logger.error(f"Failed to load configuration: {str(e)}")
    raise
