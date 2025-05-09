from sqlalchemy import Column, Text, DateTime, ForeignKey, Integer, String, Boolean
from core.database import db

Base = db.Base


class Department(Base):
    __tablename__ = "department"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=255), nullable=False)
    abbr_name = Column(String(length=100), nullable=True)
    description = Column(Text, nullable=True)
    parent_id = Column(String(255), ForeignKey("department.id"))
    status = Column(Boolean, nullable=False)
    creatcreated_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
