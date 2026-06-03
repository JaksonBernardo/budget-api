from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class StatusProjectSchema(BaseModel):

    name: str
    color: str
    is_completed: bool = False
    company_id: int



class StatusProjectPublicSchema(BaseModel):

    id: int
    name: str
    color: str
    is_completed: bool = False
    company_id: int
    created_at: datetime
    updated_at: datetime


class StatusProjectUpdateSchema(BaseModel):

    name: Optional[str] = None
    color: Optional[str] = None
    is_completed: Optional[bool] = None
    company_id: int


class ListStatusProjectPublicSchema(BaseModel):

    status: List[StatusProjectPublicSchema]
    offset: int
    limit: int
