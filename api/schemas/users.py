from typing import Optional, List
from pydantic import BaseModel, field_validator, EmailStr
from datetime import datetime


class UserCreateSchema(BaseModel):

    name: str
    email: EmailStr
    password: str
    whatsapp: Optional[str] = None
    photo: Optional[str] = None
    profile: Optional[int] = None
    company_id: int

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, value: str) -> str:

        if not value.strip():

            raise ValueError("Nome não pode estar vazio")

        return value.strip()

    @field_validator("password")
    @classmethod
    def password_min_length(cls, value: str) -> str:

        if len(value) < 6:

            raise ValueError("Senha deve ter no mínimo 6 caracteres")

        return value

    @field_validator("company_id")
    @classmethod
    def validate_company_id(cls, value: int) -> int:

        if value <= 0:

            raise ValueError("company_id deve ser maior que zero")

        return value


class UserUpdateSchema(BaseModel):

    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    whatsapp: Optional[str] = None
    photo: Optional[str] = None
    profile: Optional[int] = None

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, value: str | None) -> str | None:

        if value is not None and not value.strip():

            raise ValueError("Nome não pode estar vazio")

        return value.strip() if value else value

    @field_validator("password")
    @classmethod
    def password_min_length(cls, value: str | None) -> str | None:
        
        if value is not None and len(value) < 6:
            
            raise ValueError("Senha deve ter no mínimo 6 caracteres")
            
        return value


class UserPublicSchema(BaseModel):

    id: int
    name: str
    email: str
    whatsapp: Optional[str]
    photo: Optional[str]
    profile: Optional[int]
    company_id: int
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        from_attributes = True


class ListUserPublicSchema(BaseModel):

    users: List[UserPublicSchema]
