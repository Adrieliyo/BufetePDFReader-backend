from fastapi import Request, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from app.utils.jwt_utils import verify_token
from typing import Optional
from os import getenv

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

async def authRequired(request: Request):
    try:
        # Obtener token de la cookie
        token = request.cookies.get("token")
        
        if not token:
            raise HTTPException(
                status_code=401,
                detail="No token, authorization denied"
            )
            
        # Verificar token
        user = verify_token(token)
        
        # Agregar información del usuario a la request
        request.state.user = user
        
        return user
        
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid token or session expired"
        )