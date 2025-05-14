import psycopg2
from domain.interfaces.repositories.deparment_factory_role_repository import (
    IDepartmentFactoryRoleRepository,
)


class DepartmentFactoryRoleRepository(IDepartmentFactoryRoleRepository):
    def __init__(self, conn: psycopg2.extensions.connection):
        self.conn = conn

    def check_department_factory_role_exists(
        self, department_id: int, factory_id: int, role_id: int
    ) -> bool:
        query = """
            SELECT COUNT(*)
            FROM department_factory_role
            WHERE department_id = %s AND factory_id = %s AND role_id = %s
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (department_id, factory_id, role_id))
            return cur.fetchone()[0] > 0

    def create_department_factory_role(
        self, department_id: int, factory_id: int, role_id: int
    ) -> int:
        pass
