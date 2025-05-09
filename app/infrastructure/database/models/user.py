from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
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
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),  # gán tại DB
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),  # gán lần đầu
        onupdate=func.now(),  # gán mỗi lần UPDATE
    )
