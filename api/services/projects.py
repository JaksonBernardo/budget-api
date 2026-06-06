import pytz
import asyncio
from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import Project, ProjectService as ProjectServiceModel
from api.repositories import (
    CompanyRepository,
    ClientRepository,
    PrecificationServiceRepository,
    ProjectRepository,
    ProjectServiceRepository
)
from api.schemas import (
    ProjectSchema,
    ProjectServiceSchema,
    ProjectPublicSchema,
    ProjectServicePublicSchema,
    ProjectUpdateSchema,
    ListProjectPublicSchema
)
from api.exceptions import (
    ProjectInvalidOs,
    ProjectNotFound,
    CompanyNotFound,
    ClientNotFound,
    ServiceNotFound
)


class ProjectService:

    def __init__(
        self, 
        company_repository: CompanyRepository,
        client_repository: ClientRepository,
        precification_repository: PrecificationServiceRepository,
        project_repository: ProjectRepository,
        project_service_repository: ProjectServiceRepository,
        db: AsyncSession
    ) -> None:
        
        self.__company_repository = company_repository
        self.__client_repository = client_repository
        self.__precification_repository = precification_repository
        self.__project_repository = project_repository
        self.__project_service_repository = project_service_repository
        self.__db = db

    
    async def create(self, project_data: ProjectSchema) -> Project:

        try:

            company, client = await asyncio.gather(
                self.__company_repository.get_by_id(project_data.company_id),
                self.__client_repository.get_by_id(project_data.client_id)
            )

            if not company: raise CompanyNotFound()

            if not client: raise ClientNotFound()

            project_services_rows = []

            if project_data.services:

                service_ids = {
                    item.service_id
                    for item in project_data.services
                }

                services = await self.__precification_repository.get_by_ids(
                    project_data.company_id,
                    service_ids
                )

                if len(services) != len(service_ids): raise ServiceNotFound()

                services_map = {s.id : s for s in services}

                for serv in project_data.services:

                    service_entity = services_map[serv.service_id]

                    project_services_rows.append({
                        "service_id": service_entity.id,
                        "service_name": serv.service_name,
                        "service_qtd": serv.service_qtd,
                        "service_value": serv.service_value,
                        "service_total_value": serv.service_qtd * serv.service_value,
                        "start_date": project_data.start_date,
                        "delivery_date": None
                    })

                _BRAZIL_TIMEZONE_ = pytz.timezone("America/Sao_Paulo")

                project_entity = Project(
                    budget_id = project_data.budget_id,
                    client_id = project_data.client_id,
                    code = project_data.code,
                    origin = project_data.origin,
                    campaign = project_data.campaign,
                    company_id = project_data.company_id,
                    status_id = project_data.status_id,
                    start_date = project_data.start_date,
                    estimated_end_date = project_data.estimated_end_date,
                    end_date = project_data.end_date,
                    notes = project_data.notes,
                    created_at = datetime.now(_BRAZIL_TIMEZONE_),
                    updated_at = datetime.now(_BRAZIL_TIMEZONE_)
                )

                project = await self.__project_repository.save(project_entity)

                for row in project_services_rows:

                    row["project_id"] = project.id

                if project_services_rows:

                    await self.__project_service_repository.save(project_services_rows)

                await self.__db.commit()

                return await self.__project_repository.get_by_id(project.company_id, project.id)


        except Exception as ex:

            await self.__db.rollback()

            raise



