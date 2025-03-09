from pydantic import BaseModel, EmailStr
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from os import getenv
from dotenv import load_dotenv

load_dotenv()  # Cargar variables de entorno desde .env

# Configuración de SMTP
conf = ConnectionConfig(
    MAIL_USERNAME=getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=getenv("MAIL_PASSWORD"),
    MAIL_FROM=getenv("MAIL_FROM"),
    MAIL_PORT=int(getenv("MAIL_PORT")),
    MAIL_SERVER=getenv("MAIL_SERVER"),
    MAIL_STARTTLS=True,     # Nuevo nombre para TLS
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

# Función para enviar el correo de verificación
async def send_verification_email(email: EmailStr, token: str):
    verification_url = f"http://localhost:8000/auth/verify?token={token}"
    message = MessageSchema(
        subject="Account Verification",
        recipients=[email],
        body=f"Click the link to verify your account: {verification_url}",
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)