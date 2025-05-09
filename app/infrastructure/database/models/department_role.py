from sqlalchemy import Column, DateTime, Integer, ForeignKey
from core.database import db

Base = db.Base


class DepartmentRole(Base):
    __tablename__ = "department_role"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("role.id"))
    deparment_id = Column(Integer, ForeignKey("department.id"))
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
