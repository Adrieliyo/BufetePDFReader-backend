from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
import smtplib
from email.message import EmailMessage
from os import getenv
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/mail", tags=["Mail Testing"])

# Configuración de credenciales (asegúrate de protegerlas en variables de entorno)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = getenv("GMAIL_USER")  # Tu correo Gmail
EMAIL_PASSWORD = getenv("GMAIL_PASS")  # Tu contraseña o contraseña de aplicación

class EmailSchema(BaseModel):
    recipient: EmailStr
    subject: str
    content: str

def send_email(email_data: EmailSchema):
    try:
        msg = EmailMessage()
        msg["From"] = EMAIL_SENDER
        msg["To"] = email_data.recipient
        msg["Subject"] = email_data.subject
        msg.set_content(email_data.content)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Seguridad
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)  # Autenticación
            server.send_message(msg)  # Enviar correo
        
        return {"message": "Correo enviado correctamente"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error enviando correo: {str(e)}")

@router.post("/send-email")
def send_email_endpoint(email_data: EmailSchema):
    return send_email(email_data)