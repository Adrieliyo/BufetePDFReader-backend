import jwt
from datetime import datetime, timedelta
from os import getenv
from app.utils.timezone import TIMEZONE

def generate_verification_token(user_id: int) -> str:
    secret_key = getenv("SECRET_KEY")
    secret_algorithm = getenv("SECRET_ALGORITHM")

    current_time = datetime.now(TIMEZONE)
    expiration = current_time + timedelta(hours=24)
    
    token_data = {
        "user_id": user_id,
        "exp": expiration
    }
    
    return jwt.encode(token_data, secret_key, secret_algorithm)

def verify_token(token: str):
    try:
        secret_key = getenv("SECRET_KEY")
        secret_algorithm = getenv("SECRET_ALGORITHM")
        
        payload = jwt.decode(token, secret_key, algorithms=[secret_algorithm])
        
        # Extraer user_id del token
        user_id = payload.get("user_id")
        
        return user_id
    except jwt.ExpiredSignatureError:
        # Token ha expirado
        return None
    except jwt.InvalidTokenError:
        # Token inválido
        return None