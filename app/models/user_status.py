from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.config.database import Base

class UserStatus(Base):
    __tablename__ = "user_status"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    status = Column(String, unique=True, nullable=False)

    users = relationship("User", back_populates="status")