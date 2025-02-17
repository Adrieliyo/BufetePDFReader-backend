import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

# Obtener la URL de la base de datos desde el .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Configurar SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Importar todos los modelos aquí
from app.models.users import User
from app.models.roles import Role
from app.models.user_status import UserStatus
from app.models.password_resets import PasswordReset

# Crear todas las tablas
Base.metadata.create_all(bind=engine)