import bcrypt

def hash_password(password: str) -> str:
    # Convertir la contraseña a bytes
    password_bytes = password.encode('utf-8')
    # Generar el salt y hacer el hash
    salt = bcrypt.gensalt()
    # Generar el hash
    hashed = bcrypt.hashpw(password_bytes, salt)
    # Retornar el hash como string
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Convertir las contraseñas a bytes
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    # Verificar el hash
    return bcrypt.checkpw(password_bytes, hashed_bytes)