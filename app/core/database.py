from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from typing import Generator
import logging
from .config import config

# Configure logging
logger = logging.getLogger("uvicorn")


class Database:
    """
    Database connection and session management class.
    """

    def __init__(self, db_url: str):
        self.engine = create_engine(
            db_url,
            echo=False,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
        )
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
        )
        self.Base = declarative_base()

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        """
        Context manager for database sessions.
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {str(e)}")
            raise
        finally:
            session.close()

    def get_db(self) -> Generator[Session, None, None]:
        """
        FastAPI dependency to provide a database session.
        """
        with self.session() as session:
            yield session

    def test_connection(self) -> bool:
        """
        Test database connection.
        """
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info(
                f"[DATABASE]:: Connected to database '{config.database.DB_NAME}' successfully"
            )
            return True
        except SQLAlchemyError as e:
            logger.error(f"[DATABASE]:: Connection failed: {str(e)}")
            return False


# Initialize the database instance (used across the app)
db = Database(db_url=config.database.database_uri)
