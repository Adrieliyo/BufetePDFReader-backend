from pydantic import BaseModel, EmailStr
from typing import Optional

# Esquema base (para evitar duplicación de código)
class UserBase(BaseModel):
    username: str
    email: EmailStr

# Esquema para crear un usuario (incluye contraseña)
class UserCreate(BaseModel):
    username: str
    names: str
    lastnames: str
    email: EmailStr
    password: str

# Esquema para leer un usuario (excluye contraseña)
class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True  # Permite usar modelos de SQLAlchemy como respuesta

# Esquema para actualizar un usuario (todos los campos opcionales)
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    names: Optional[str] = None
    lastnames: Optional[str] = None