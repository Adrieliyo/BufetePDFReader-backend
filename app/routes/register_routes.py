from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.schemas.user_schema import UserCreate
from app.models.users import User
from app.utils.password_utils import hash_password
from app.utils.verification_token import generate_verification_token, verify_token
from app.config.mail_config import send_verification_email_smtp

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
async def register_user(
    user_data: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    try:
        # Check if email already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Este correo electrónico ya está registrado"
            )
        
         # Check if username already exists
        existing_username = db.query(User).filter(User.username == user_data.username).first()
        if existing_username:
            raise HTTPException(
                status_code=400,
                detail="El nombre de usuario ya ha sido tomado"
            )

        # Hash password
        hashed_password = hash_password(user_data.password)

        # Create new user
        new_user = User(
            username=user_data.username,
            names=user_data.names,
            lastnames=user_data.lastnames,
            email=user_data.email,
            password=hashed_password,
            role_id=2,  # Client role
            status_id=2  # Inactive until verified
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Generar token de verificación
        verification_token = generate_verification_token(new_user.id)

        # Añadir tarea de envío de correo en segundo plano
        background_tasks.add_task(
            send_verification_email_smtp, 
            email=new_user.email, 
            token=verification_token,
            username=new_user.username
        )

        return {
            "message": "Usuario creado exitosamente. Por favor, revisa tu correo electrónico para verificar tu cuenta.",
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email
            }
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error al crear nuevo usuario: {str(e)}"
        )

@router.get("/verify")
async def verify_email(token: str, db: Session = Depends(get_db)):
    try:
        # Verificar token y obtener ID de usuario
        user_id = verify_token(token)
        
        if not user_id:
            raise HTTPException(
                status_code=400,
                detail="Token inválido o expirado"
            )
        
        # Buscar usuario
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )
        
        # Verificar si el usuario ya está activado
        if user.status_id == 1:
            raise HTTPException(
                status_code=400,
                detail="Este usuario ya ha sido activado"
            )
        
        # Actualizar estado del usuario a activo
        user.status_id = 1  # Estado activo
        db.commit()
        
        return {
            "message": "Cuenta verificada exitosamente",
            "username": user.username
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al verificar cuenta: {str(e)}"
        )