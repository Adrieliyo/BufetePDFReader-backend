from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, text
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from app.config.database import Base
from app.utils.timezone import TimezoneAware

class PasswordReset(Base):
    __tablename__ = "passwordresets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    reset_code = Column(String(6), nullable=False)
    expires_at = Column(TimezoneAware, nullable=False)
    is_used = Column(Boolean, default=False)
    created_at = Column(TimezoneAware, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    updated_at = Column(TimezoneAware, server_default=text("CURRENT_TIMESTAMP"), 
                       onupdate=text("CURRENT_TIMESTAMP"), nullable=False)
    is_activated = Column(Boolean, default=False)

    # Relación con el modelo User
    user = relationship("User", back_populates="password_resets")