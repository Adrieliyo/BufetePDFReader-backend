from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse 
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth_schema import LoginData
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.config.database import SessionLocal
from app.models.users import User
from app.utils.password_utils import verify_password
from app.utils.jwt_utils import create_access_token
from typing import Optional
from datetime import datetime, timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
async def login(
    login_data: LoginData,
    db: Session = Depends(get_db)
):
    try:
        # Buscar usuario por email o username
        user = db.query(User).filter(
            or_(
                User.email == login_data.email_or_username,
                User.username == login_data.email_or_username
            )
        ).first()

        if not user:
            raise HTTPException(
                status_code=400,
                detail="User not found"
            )

        # Verificar contraseña
        if not verify_password(login_data.password, user.password):
            raise HTTPException(
                status_code=400,
                detail="Password incorrect"
            )

        # Verificar estado de la cuenta
        if user.status_id == 2:
            raise HTTPException(
                status_code=403,
                detail="Please activate your account via the email sent to you."
            )
        elif user.status_id == 3:
            raise HTTPException(
                status_code=403,
                detail="Your account is suspended and cannot be accessed at this time."
            )
        elif user.status_id != 1:
            raise HTTPException(
                status_code=403,
                detail="Your account status is not valid for access."
            )

        # Crear token
        token_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role_id": user.role_id
        }
        
        access_token = create_access_token(token_data)

        # Crear respuesta JSON
        response = JSONResponse(content={
            "id": user.id,
            "username": user.username,
            "names": user.names,
            "lastnames": user.lastnames,
            "email": user.email,
            "role_id": user.role_id,
            "status_id": user.status_id
        })

        # Configurar cookie correctamente
        response.set_cookie(
            key="token",
            value=access_token,
            httponly=True,
            secure=False,  # Cambiar a True en producción con HTTPS
            samesite="lax",
            max_age=3600  # 1 hora
        )

        return response

        # Crear respuesta
        # response = Response()
        
        # # Configurar cookie
        # response.set_cookie(
        #     key="token",
        #     value=access_token,
        #     httponly=True,
        #     secure=False,  # Cambiar a True en producción con HTTPS
        #     samesite="lax",
        #     max_age=3600  # 1 hora
        # )

        # # Devolver datos del usuario
        # return {
        #     "id": user.id,
        #     "username": user.username,
        #     "names": user.names,
        #     "lastnames": user.lastnames,
        #     "email": user.email,
        #     "role_id": user.role_id,
        #     "status_id": user.status_id,
        #     "access_token": access_token,
        #     "token_type": "bearer"
        # }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong: {str(e)}"
        )

@router.post("/logout")
async def logout():
    response = JSONResponse(content={"message": "Logout successful"})
    response.delete_cookie("token")
    return response