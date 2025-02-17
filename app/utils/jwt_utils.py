from datetime import datetime, timedelta
from typing import Dict
import jwt
from os import getenv
from fastapi import HTTPException

def create_access_token(data: Dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=1)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        getenv("SECRET_KEY"),
        algorithm=getenv("SECRET_ALGORITHM")
    )
    
    return encoded_jwt

def verify_token(token: str) -> Dict:
    try:
        payload = jwt.decode(
            token,
            getenv("SECRET_KEY"),
            algorithms=[getenv("SECRET_ALGORITHM")]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )