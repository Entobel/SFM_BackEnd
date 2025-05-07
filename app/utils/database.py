from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from typing import Generator
import logging
from .config import config

# Configure logging
logger = logging.getLogger(__name__)

class Database:
    """
    Database connection and session management class.
    
    This class handles database connections, session management, and provides
    utility methods for database operations.
    """
    
    def __init__(self, db_url: str):
        """
        Initialize database connection and session factory.
        
        Args:
            db_url (str): Database connection URL
        """
        self.engine = create_engine(
            db_url,
            echo=False,  # Disable SQL logging
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10
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
        
        Yields:
            Session: SQLAlchemy database session
            
        Example:
            with db.session() as session:
                session.query(User).all()
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
        FastAPI dependency for database sessions.
        
        Yields:
            Session: SQLAlchemy database session for use in FastAPI endpoints
        """
        with self.session() as session:
            yield session

    def test_connection(self) -> bool:
        """
        Test database connection by executing a simple query.
        
        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except SQLAlchemyError as e:
            logger.error(f"Database connection failed: {str(e)}")
            return False


# Initialize database instance
db = Database(db_url=config.database.database_uri)
