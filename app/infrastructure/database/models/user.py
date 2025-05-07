from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from core.database import db

Base = db.Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=True)
    phone = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    department_factory_id = Column(Integer, ForeignKey("department_factory.id"))
    department_role_id = Column(Integer, ForeignKey("department_role.id"))
    status = Column(Boolean)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
