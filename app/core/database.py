import logging
from contextlib import contextmanager
from typing import Generator
from psycopg2 import pool
import psycopg2
from loguru import logger
from app.core.config import config



class Database:
    def __init__(self, db_url: str):
        masked_url = db_url.replace(config.database.DB_PASSWORD, "***")
        logger.info(f"[DATABASE]:: Connecting to {masked_url}")

        try:
            self.connection_pool = pool.SimpleConnectionPool(
                minconn=1, maxconn=15, dsn=db_url
            )
            if self.connection_pool:
                logger.info("[DATABASE]:: Connection pool created successfully")
        except psycopg2.OperationalError as e:
            logger.error("[DATABASE]:: Failed to create connection pool", exc_info=True)
            raise

    def _set_timezone(self, conn):
        with conn.cursor() as cursor:
            cursor.execute("SHOW TIME ZONE")
            current_tz = cursor.fetchone()[0]
            if current_tz != "Asia/Ho_Chi_Minh":
                cursor.execute("SET TIME ZONE 'Asia/Ho_Chi_Minh'")
                logger.info(f"[DATABASE]:: Timezone set to Asia/Ho_Chi_Minh")

    @contextmanager
    def session(self) -> Generator[psycopg2.extensions.connection, None, None]:
        conn = None
        try:
            conn = self.connection_pool.getconn()
            self._set_timezone(conn)
            yield conn
            conn.commit()
        except Exception:
            if conn:
                conn.rollback()
            logger.error("Database session error:", exc_info=True)
            raise
        finally:
            if conn:
                self.connection_pool.putconn(conn)

    def test_connection(self) -> bool:
        try:
            with self.session() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
                    result = cur.fetchone()
                    logger.info(
                        f"Connected to DB '{config.database.DB_NAME}' successfully"
                    )
                    return result == (1,)
        except Exception:
            logger.error("[DATABASE]:: Connection test failed", exc_info=True)
            return False

    def get_db(self):
        conn = self.connection_pool.getconn()
        try:
            self._set_timezone(conn)
            yield conn
            conn.commit()  # Commit luôn sau mỗi request
        except Exception:
            conn.rollback()
            raise
        finally:
            self.connection_pool.putconn(conn)


# Global instance (use across the app)
db = Database(db_url=config.database.database_uri)
