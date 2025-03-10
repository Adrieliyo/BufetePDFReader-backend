from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import and_, not_, func
from app.config.database import SessionLocal
from app.models.users import User
from app.models.password_resets import PasswordReset
from app.utils.password_utils import hash_password
from app.config.mail_config import send_password_reset_email
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timedelta
from typing import Optional
import random
import string
from app.utils.timezone import TIMEZONE

router = APIRouter(prefix="/password", tags=["Password Reset"])

# Schemas
class RequestResetSchema(BaseModel):
    email: EmailStr

class VerifyCodeSchema(BaseModel):
    email: EmailStr
    code: str = Field(..., min_length=6, max_length=6)

class ResetPasswordSchema(BaseModel):
    email: EmailStr
    code: str = Field(..., min_length=6, max_length=6)
    new_password: str = Field(..., min_length=8)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_reset_code():
    """Genera un código numérico de 6 caracteres"""
    return ''.join(random.choice(string.digits) for _ in range(6))

@router.post("/request-reset")
async def request_password_reset(
    request: RequestResetSchema,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    try:
        # Buscar al usuario
        user = db.query(User).filter(User.email == request.email).first()

        # Siempre devolvemos el mismo mensaje por seguridad
        success_message = {
            "message": "Si el correo existe, recibirás un código de recuperación"
        }

        # Si el usuario no existe, devolvemos el mensaje de éxito igualmente
        if not user:
            return success_message

        # Verificar intentos recientes (últimas 24 horas)
        one_day_ago = datetime.now(TIMEZONE) - timedelta(hours=24)
        recent_attempts = db.query(PasswordReset).filter(
            PasswordReset.id_user == user.id,
            PasswordReset.created_at >= one_day_ago
        ).count()

        if recent_attempts >= 3:
            return HTTPException(
                status_code=400,
                detail="Has excedido el número máximo de intentos. Intenta nuevamente en 24 horas"
            )

        # Verificar si existe un código válido y no usado
        current_time = datetime.now(TIMEZONE)
        existing_reset = db.query(PasswordReset).filter(
            PasswordReset.id_user == user.id,
            PasswordReset.expires_at > current_time,
            PasswordReset.is_used == False
        ).first()

        if existing_reset:
            return HTTPException(
                status_code=400,
                detail="Ya tienes un código de recuperación válido. Revisa tu correo o espera a que expire"
            )

        # Generar nuevo código
        recovery_code = generate_reset_code()
        
        # Crear nuevo registro de reseteo
        new_reset = PasswordReset(
            id_user=user.id,
            reset_code=recovery_code,
            expires_at=datetime.now(TIMEZONE) + timedelta(minutes=15),  # 15 minutos
            is_used=False,
            is_activated=False
        )
        
        db.add(new_reset)
        db.commit()
        
        # Enviar correo en segundo plano
        background_tasks.add_task(
            send_password_reset_email,
            email=user.email,
            code=recovery_code,
            username=user.username
        )

        return success_message

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar la solicitud: {str(e)}"
        )


@router.post("/verify-code")
async def verify_reset_code(
    request: VerifyCodeSchema,
    db: Session = Depends(get_db)
):
    try:
        # Buscar al usuario
        user = db.query(User).filter(User.email == request.email).first()

        if not user:
            raise HTTPException(
                status_code=400,
                detail="Código inválido"
            )

        # Buscar solicitud de reseteo
        current_time = datetime.now(TIMEZONE)
        reset_request = db.query(PasswordReset).filter(
            PasswordReset.id_user == user.id,
            PasswordReset.reset_code == request.code,
            PasswordReset.is_activated == False,
            PasswordReset.is_used == False,
            PasswordReset.expires_at > current_time
        ).first()

        if not reset_request:
            raise HTTPException(
                status_code=400,
                detail="Código inválido o expirado"
            )

        # Marcar el código como activado (verificado)
        reset_request.is_activated = True
        db.commit()

        return {
            "message": "Código verificado correctamente"
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al verificar el código: {str(e)}"
        )


@router.post("/reset")
async def reset_password(
    request: ResetPasswordSchema,
    db: Session = Depends(get_db)
):
    try:
        # Buscar al usuario
        user = db.query(User).filter(User.email == request.email).first()

        if not user:
            raise HTTPException(
                status_code=400,
                detail="Datos inválidos"
            )

        # Buscar solicitud de reseteo
        current_time = datetime.now(TIMEZONE)
        reset_request = db.query(PasswordReset).filter(
            PasswordReset.id_user == user.id,
            PasswordReset.reset_code == request.code,
            PasswordReset.is_used == False,
            PasswordReset.is_activated == True,
            PasswordReset.expires_at > current_time
        ).first()

        if not reset_request:
            raise HTTPException(
                status_code=400,
                detail="Código inválido o expirado"
            )

        # Hash de la nueva contraseña
        hashed_password = hash_password(request.new_password)

        # Actualizar contraseña
        user.password = hashed_password

        # Marcar código como usado
        reset_request.is_used = True

        # Invalidar todos los otros códigos activos del usuario
        other_requests = db.query(PasswordReset).filter(
            PasswordReset.id_user == user.id,
            PasswordReset.id != reset_request.id
        ).all()
        
        for req in other_requests:
            req.is_used = True

        db.commit()

        return {
            "message": "Contraseña actualizada correctamente"
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar la contraseña: {str(e)}"
        )