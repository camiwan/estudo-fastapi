from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from app.db.database import Base

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)