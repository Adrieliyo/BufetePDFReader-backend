from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from app.config.database import SessionLocal
from app.schemas.user_schema import UserUpdate
from app.models.users import User
from app.middlewares.auth_required import authRequired
from typing import List
import os
import shutil
from datetime import datetime

router = APIRouter(prefix="/users", tags=["Users"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/user-data")
async def get_user_data(
    current_user = Depends(authRequired),
    db: Session = Depends(get_db)
):
    try:
        user = db.query(User).filter(User.id == current_user["id"]).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        return {
            "id": user.id,
            "username": user.username,
            "names": user.names,
            "lastnames": user.lastnames,
            "email": user.email,
            "role_id": user.role_id,
            "status_id": user.status_id,
            "profile_image": user.profile_image if hasattr(user, 'profile_image') else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload-image")
async def upload_profile_image(
    file: UploadFile = File(...),
    current_user = Depends(authRequired),
    db: Session = Depends(get_db)
):
    try:
        # Verificar tipo de archivo
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")

        # Crear directorio si no existe
        upload_dir = "uploads/profile_images"
        os.makedirs(upload_dir, exist_ok=True)

        # Generar nombre único para el archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = os.path.splitext(file.filename)[1]
        filename = f"profile_{current_user['id']}_{timestamp}{file_extension}"
        file_path = os.path.join(upload_dir, filename)

        # Guardar archivo
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Actualizar ruta en la base de datos
        user = db.query(User).filter(User.id == current_user["id"]).first()
        if hasattr(user, 'profile_image'):
            # Eliminar imagen anterior si existe
            old_image = user.profile_image
            if old_image and os.path.exists(old_image):
                os.remove(old_image)
            
        user.profile_image = file_path
        db.commit()

        return {"message": "Profile image uploaded successfully", "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/image/{user_id}")
async def get_user_image(
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not hasattr(user, 'profile_image') or not user.profile_image:
            raise HTTPException(status_code=404, detail="Image not found")

        return FileResponse(user.profile_image)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/my-image")
async def get_my_image(
    current_user = Depends(authRequired),
    db: Session = Depends(get_db)
):
    try:
        user = db.query(User).filter(User.id == current_user["id"]).first()
        if not user or not hasattr(user, 'profile_image') or not user.profile_image:
            raise HTTPException(status_code=404, detail="Profile image not found")

        return FileResponse(user.profile_image)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/all")
async def get_all_users(
    current_user = Depends(authRequired),
    db: Session = Depends(get_db)
):
    try:
        # Verificar si es administrador
        if current_user["role_id"] != 1:
            raise HTTPException(
                status_code=403,
                detail="Not authorized to view all users"
            )

        users = db.query(User).all()
        return [
            {
                "id": user.id,
                "username": user.username,
                "names": user.names,
                "lastnames": user.lastnames,
                "email": user.email,
                "role_id": user.role_id,
                "status_id": user.status_id
            } for user in users
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update")
async def update_user(
    user_data: UserUpdate,
    current_user = Depends(authRequired),
    db: Session = Depends(get_db)
):
    try:
        user = db.query(User).filter(User.id == current_user["id"]).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Actualizar campos si están presentes en la solicitud
        if user_data.username:
            # Verificar si el nuevo username ya existe
            existing = db.query(User).filter(
                User.username == user_data.username,
                User.id != current_user["id"]
            ).first()
            if existing:
                raise HTTPException(status_code=400, detail="Username already taken")
            user.username = user_data.username

        if user_data.email:
            # Verificar si el nuevo email ya existe
            existing = db.query(User).filter(
                User.email == user_data.email,
                User.id != current_user["id"]
            ).first()
            if existing:
                raise HTTPException(status_code=400, detail="Email already registered")
            user.email = user_data.email

        db.commit()
        db.refresh(user)

        return {
            "message": "User updated successfully",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/deactivate/{user_id}")
async def suspend_user(
    user_id: int,
    current_user = Depends(authRequired),
    db: Session = Depends(get_db)
):
    try:
        # Verificar si es administrador
        if current_user["role_id"] != 1:
            raise HTTPException(
                status_code=403,
                detail="Not authorized to deactivate users"
            )

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Cambiar estado a inactivo (2)
        user.status_id = 2
        db.commit()

        return {"message": f"User {user.username} has been deactivated"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))