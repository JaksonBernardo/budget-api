from typing import Optional, List
from pydantic import BaseModel, field_validator
from datetime import datetime

from api.exceptions.segments import SegmentInvalidName
from api.exceptions.companys import InvalidTypeCompanyId, ZeroCompanyId

class SegmentSchema(BaseModel):

    name: str
    contract: Optional[str]
    company_id: int
    created_at: datetime
    updated_at: datetime

    @field_validator("name")
    def validate_name(cls, value):

        if not value:

            raise SegmentInvalidName()
        
        return value
    
    @field_validator("company_id")
    def validate_company_id(cls, value):

        if type(value) is not int:

            raise InvalidTypeCompanyId()
        
        if value <= 0:

            raise ZeroCompanyId()
        
        return value
    
class SegmentPublicSchema(BaseModel):

    id: int
    name: str
    contract: str
    company_id: int
    created_at: datetime
    updated_at: datetime
    

class SegmentUpdateSchema(BaseModel):

    name: Optional[str]
    contract: Optional[str]
    company_id: Optional[int]
    updated_at: Optional[datetime]

    @field_validator("name")
    def validate_name(cls, value):

        if not value:

            raise SegmentInvalidName()
        
        return value
    
    @field_validator("company_id")
    def validate_company_id(cls, value):

        if type(value) is not int:

            raise InvalidTypeCompanyId()
        
        if value <= 0:

            raise ZeroCompanyId()
        
        return value


class ListSegmentPublicSchema(BaseModel):

    segments: List[SegmentPublicSchema]
    limit: int
    offset: int


