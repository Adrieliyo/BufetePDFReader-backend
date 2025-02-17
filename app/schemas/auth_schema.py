from pydantic import BaseModel

class LoginData(BaseModel):
    email_or_username: str
    password: str