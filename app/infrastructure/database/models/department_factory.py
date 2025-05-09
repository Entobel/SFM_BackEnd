from sqlalchemy import Column, DateTime, Integer, ForeignKey
from core.database import db

Base = db.Base


class DepartmentFactory(Base):
    __tablename__ = "department_factory"

    id = Column(Integer, primary_key=True, index=True)
    factory_id = Column(Integer, ForeignKey("factory.id"))
    deparment_id = Column(Integer, ForeignKey("department.id"))
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
