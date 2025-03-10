from pydantic import BaseModel, EmailStr
from fastapi import HTTPException
from email.message import EmailMessage
import smtplib
from os import getenv
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()  # Cargar variables de entorno desde .env

# Configuración para smtplib
SMTP_SERVER = getenv("MAIL_SERVER", "smtp.gmail.com")
SMTP_PORT = int(getenv("MAIL_PORT", "587"))
EMAIL_SENDER = getenv("GMAIL_USER") 
EMAIL_PASSWORD = getenv("GMAIL_PASS")

class EmailSchema(BaseModel):
    recipient: EmailStr
    subject: str
    content: str
    subtype: str = "plain"

# Función para enviar correo utilizando smtplib
def send_email(email_data: EmailSchema) -> Dict[str, Any]:
    try:
        msg = EmailMessage()
        msg["From"] = EMAIL_SENDER
        msg["To"] = email_data.recipient
        msg["Subject"] = email_data.subject

        # Verificar si el contenido es HTML o texto plano
        if email_data.subtype == "html":
            msg.add_alternative(email_data.content, subtype="html")
        else:
            msg.set_content(email_data.content)  # Texto plano por defecto

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Seguridad
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)  # Autenticación
            server.send_message(msg)  # Enviar correo
        
        return {"message": "Correo enviado correctamente"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error enviando correo: {str(e)}")

# Función alternativa para enviar correo de verificación mediante smtplib
def send_verification_email_smtp(email: EmailStr, token: str, username: str = None):
    verification_url = f"http://localhost:8000/auth/verify?token={token}"
    
    greeting = f"Hola {username}," if username else "Hola,"
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 5px;">
            <h2 style="color: #4a4a4a;">Verificación de Cuenta</h2>
            <p>{greeting}</p>
            <p>Gracias por registrarte. Para verificar tu cuenta, haz clic en el siguiente enlace:</p>
            <p style="text-align: center;">
                <a href="{verification_url}" 
                   style="background-color: #0066cc; color: white; padding: 10px 20px; 
                          text-decoration: none; border-radius: 5px; display: inline-block;">
                    Verificar mi cuenta
                </a>
            </p>
            <p>Si no puedes hacer clic en el botón, copia y pega esta URL en tu navegador:</p>
            <p style="word-break: break-all; background-color: #f8f8f8; padding: 10px; border-radius: 3px;">
                {verification_url}
            </p>
            <p>Si no has solicitado esta verificación, puedes ignorar este mensaje.</p>
            <p>Saludos,<br>El equipo de Bufete Estudiantil</p>
        </div>
    </body>
    </html>
    """
    
    email_data = EmailSchema(
        recipient=email,
        subject="Verificación de Cuenta - Bufete Estudiantil",
        content=html_content,
        subtype="html"
    )
    
    return send_email(email_data)