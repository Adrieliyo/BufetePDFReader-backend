from fastapi import APIRouter, HTTPException
from app.config.mail_config import EmailSchema, send_email

router = APIRouter(prefix="/mail", tags=["Mail Testing"])

@router.post("/send-email")
def send_email_endpoint(email_data: EmailSchema):
    return send_email(email_data)