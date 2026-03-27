from typing import Optional, List
from pydantic import BaseModel, field_validator, EmailStr
from datetime import datetime
from validate_docbr import CNPJ
from api.schemas import LegalEntityPublicSchema
from api.exceptions.companys import InvalidTypeCompanyId, ZeroCompanyId

cnpj_validator = CNPJ()


class ClientSchema(BaseModel):

    companie: str
    cpf_cnpj: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    address: Optional[str]
    number: Optional[int] = None
    state: Optional[str]
    cep: Optional[str]
    city: Optional[str]
    company_id: int

    @field_validator("cpf_cnpj")
    def validate_cpf_cnpj(cls, value):
        if value is None:
            return value

        if not cnpj_validator.validate(value):
            raise ValueError("CNPJ inválido")

        return value
    

    @field_validator("company_id")
    def validate_company_id(cls, value):

        if not isinstance(value, int):

            raise InvalidTypeCompanyId()
        
        if value <= 0:

            raise ZeroCompanyId()
        
        return value

class ClientPublicSchema(BaseModel):

    id: int
    id_person: int
    company_id: int
    created_at: datetime
    updated_at: datetime
    legal_entity: LegalEntityPublicSchema

    class Config:
        from_attributes = True
    

class ClientUpdateSchema(BaseModel):

    companie: Optional[str]
    cpf_cnpj: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    address: Optional[str]
    number: Optional[int] = None
    state: Optional[str]
    cep: Optional[str]
    city: Optional[str]
    company_id: int

    @field_validator("cpf_cnpj")
    def validate_cpf_cnpj(cls, value):
        if value is None:
            return value

        if not cnpj_validator.validate(value):
            raise ValueError("CNPJ inválido")

        return value
    

    @field_validator("company_id")
    def validate_company_id(cls, value):

        if not isinstance(value, int):

            raise InvalidTypeCompanyId()
        
        if value <= 0:

            raise ZeroCompanyId()
        
        return value

class ListClientPublicSchema(BaseModel):

    clients: List[ClientPublicSchema]
    offset: int
    limit: int

