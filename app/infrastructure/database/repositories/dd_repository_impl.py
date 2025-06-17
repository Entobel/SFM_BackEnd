import psycopg2
from app.domain.interfaces.repositories.dd_repository import IDDRepository
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class DDRepository(IDDRepository):
    def __init__(self, conn: psycopg2.extensions.connection, query_helper: IQueryHelperService):
        self.conn = conn
        self.query_helper = query_helper

    def create_dd_report(self, dd_entity):
        return super().create_dd_report(dd_entity)
