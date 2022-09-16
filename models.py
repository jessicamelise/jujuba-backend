from database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False, default='salao')
    active = Column(Boolean, nullable=False, default=True)