from typing import Optional, List
from pydantic import BaseModel, field_validator, EmailStr
from datetime import datetime


class LegalEntityPublicSchema(BaseModel):

    id: int
    companie: str
    cpf_cnpj: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    address: Optional[str]
    number: Optional[int] = None
    state: Optional[str]
    cep: Optional[str]
    city: Optional[str]

    class Config:
        from_attributes = True

    