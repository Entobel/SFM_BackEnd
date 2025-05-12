from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, VARCHAR
from core.database import db

Base = db.Base


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(255))
    description = Column(Text)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
