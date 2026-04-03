from pydantic import BaseModel, EmailStr, field_validator

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginSchema(BaseModel):

    email: EmailStr
    password: str

    @field_validator("password")
    def password_min_length(cls, value):

        if len(value.strip()) < 6:
            raise ValueError("Senha deve ter pelo menos 6 caracteres")

        return value
