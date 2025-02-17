from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.schemas.user_schema import UserCreate
from app.models.users import User
from app.utils.password_utils import hash_password
# from app.utils.verification_token import generate_verification_token
# from app.config.mail_config import send_verification_email

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
    db: Session = Depends(get_db),
    # background_tasks: BackgroundTasks = Depends()
):
    try:
        # Check if email already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )
        
         # Check if username already exists
        existing_username = db.query(User).filter(User.username == user_data.username).first()
        if existing_username:
            raise HTTPException(
                status_code=400,
                detail="Username already taken"
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

        # Generate verification token
        # verification_token = generate_verification_token(new_user.id)

        # Send verification email
        # await send_account_verification(new_user.email, verification_token)
        
        # Generar token de verificación
        # verification_token = generate_verification_token(new_user.id)

        # Enviar correo en segundo plano
        # background_tasks.add_task(send_verification_email, new_user.email, verification_token)


        return {
            "message": "User created successfully. Please check your email to verify your account.",
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
            detail=f"Error creating new user: {str(e)}"
        )