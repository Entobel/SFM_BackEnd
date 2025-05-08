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
    def __init__(self, db_url: str):
        logger.info(
            f"[DATABASE]:: Connecting to {db_url.replace(config.database.DB_PASSWORD, '***')}"
        )
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
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error("Database session error:", exc_info=True)
            raise
        finally:
            session.close()

    def test_connection(self) -> bool:
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info(
                f"[DATABASE]:: Connected to DB '{config.database.DB_NAME}' successfully"
            )
            return True
        except SQLAlchemyError as e:
            logger.error("[DATABASE]:: Connection failed:", exc_info=True)
            return False

    def get_db(self) -> Generator[Session, None, None]:
        """
        FastAPI-compatible dependency for database session.
        Use as: `db: Session = Depends(db.get_db)`
        """
        db_session = self.SessionLocal()
        try:
            yield db_session
        finally:
            db_session.close()


# Global instance (use across the app)
db = Database(db_url=config.database.database_uri)
