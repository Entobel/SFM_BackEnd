from sqlalchemy import Column, Text, DateTime, VARCHAR, Integer, String, Boolean
from core.database import db

Base = db.Base


class Factory(Base):
    __tablename__ = "factory"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=255), nullable=False)
    abbr_name = Column(String(length=100), nullable=True)
    description = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    address = Column(Text, nullable=False)
    status = Column(Boolean, nullable=False)
    creatcreated_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
