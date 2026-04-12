from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, field_validator, EmailStr, ConfigDict
from pydantic.functional_validators import model_validator


class CompanySchema(BaseModel):

    photo: Optional[str] = None
    email: EmailStr
    name: str
    address: Optional[str] = None
    number: Optional[int] = None
    state: Optional[str] = None
    cep: Optional[str] = None
    city: Optional[str] = None
    cnpj: str
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    website: Optional[str] = None
    is_blocked: bool = False
    plan_id: int


class CompanyUpdateSchema(BaseModel):

    photo: Optional[str] = None
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    address: Optional[str] = None
    number: Optional[int] = None
    state: Optional[str] = None
    cep: Optional[str] = None
    city: Optional[str] = None
    cnpj: Optional[str] = None
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    website: Optional[str] = None
    is_blocked: Optional[bool] = None
    plan_id: Optional[int] = None


class CompanyPublicSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: Optional[str] = None
    photo: Optional[str] = None
    email: EmailStr
    name: str
    address: Optional[str] = None
    number: Optional[int] = None
    state: Optional[str] = None
    cep: Optional[str] = None
    city: Optional[str] = None
    cnpj: str
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    website: Optional[str] = None
    is_blocked: bool
    plan_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime


class ListCompanyPublicSchema(BaseModel):

    companys: List[CompanyPublicSchema]

