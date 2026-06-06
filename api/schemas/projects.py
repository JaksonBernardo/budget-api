from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, date
from decimal import Decimal

from api.models import ProjectOrigin
from api.exceptions.companys import InvalidTypeCompanyId, ZeroCompanyId



class ProjectServiceSchema(BaseModel):

    service_id: int
    service_name: str
    service_qtd: int
    service_value: Decimal = Field(ge = 0, max_digits = 12, decimal_places = 2)



class ProjectServicePublicSchema(ProjectServiceSchema):

    id: int
    service_total_value: Decimal = Field(ge = 0, max_digits = 12, decimal_places = 2)
    start_date: Optional[date] = None
    delivery_date: Optional[date] = None



class ProjectSchema(BaseModel):

    budget_id: Optional[int] = None
    client_id: int
    code: str
    origin: ProjectOrigin
    campaign: Optional[int] = 1
    company_id: int
    status_id: int
    start_date: date
    estimated_end_date: Optional[date] = None
    end_date: Optional[date] = None
    notes: Optional[str] = None

    services: List[ProjectServiceSchema] = []



class ProjectUpdateSchema(ProjectSchema):

    id: int



class ProjectPublicSchema(ProjectSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    services: List[ProjectServicePublicSchema] = []
    created_at: datetime
    updated_at: datetime



class ListProjectPublicSchema(BaseModel):

    projects: List[ProjectPublicSchema]
    limit: int
    offset: int



