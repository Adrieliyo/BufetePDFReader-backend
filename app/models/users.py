from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, text
from sqlalchemy.sql import func
from sqlalchemy.orm import validates, relationship
from app.config.database import Base
from app.utils.timezone import TimezoneAware

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    names = Column(String, nullable=False)
    lastnames = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    status_id = Column(Integer, ForeignKey('user_status.id'), nullable=False)
    created_at = Column(TimezoneAware, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    updated_at = Column(TimezoneAware, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"), nullable=False)
    profile_image = Column(String, nullable=True)

    # Relaciones
    role = relationship("Role", back_populates="users")
    status = relationship("UserStatus", back_populates="users")
    password_resets = relationship("PasswordReset", back_populates="user")