from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, delete, update, insert
from sqlalchemy.orm import selectinload
from api.models import Project, ProjectService, ProjectServiceMaterial



class ProjectServiceMaterialRepository:

    def __init__(self, db: AsyncSession) -> None:

        self.__db = db

    async def save(self, list_project_service_material: List[Dict[str, Any]]) -> None:

        query = insert(ProjectServiceMaterial)

        await self.__db.execute(
            query, list_project_service_material
        )

        await self.__db.flush()



class ProjectServiceRepository:

    def __init__(self, db: AsyncSession) -> None:

        self.__db = db

    async def save(self, list_project_service: List[Dict[str, Any]]) -> None:

        if not list_project_service:
            return

        self.__db.add_all(list_project_service)
        await self.__db.flush()

    async def delete_by_project_id(self, project_id: int) -> None:

        query = delete(ProjectService).where(ProjectService.project_id == project_id)

        await self.__db.execute(query)
        await self.__db.flush()


    async def update_delivery_status(self, service_id: int, is_delivered: bool) -> ProjectService:

        query = update(ProjectService).where(
            ProjectService.id == service_id
        ).values(is_delivered = is_delivered).returning(ProjectService)

        result = await self.__db.execute(query)
        await self.__db.flush()

        return result.scalar_one()


    async def get_service_by_id(self, service_id: int) -> ProjectService | None:

        query = select(ProjectService).where(ProjectService.id == service_id)

        result = await self.__db.execute(query)

        return result.scalar_one_or_none()




class ProjectRepository:


    def __init__(self, db: AsyncSession) -> None:

        self.__db = db

    
    async def save(self, project: Project) -> Project:

        self.__db.add(project)

        await self.__db.flush()
        await self.__db.refresh(project)

        return project


    async def get_by_id(self, company_id: int, project_id: int) -> Project | None:

        query = select(Project).where(
            Project.company_id == company_id,
            Project.id == project_id
        ).options(
            selectinload(Project.services).selectinload(ProjectService.materials)
        ).execution_options(populate_existing = True)

        result = await self.__db.execute(query)

        return result.scalar_one_or_none()


    async def get_by_budget_id(self, company_id: int, budget_id: int) -> Project | None:

        query = select(Project).where(
            Project.company_id == company_id,
            Project.budget_id == budget_id
        ).options(
            selectinload(Project.services).selectinload(ProjectService.materials)
        ).execution_options(populate_existing = True)

        result = await self.__db.execute(query)

        return result.scalar_one_or_none()


    async def delete(self, company_id: int, project_id: int) -> None:

        query = delete(Project).where(
            Project.company_id == company_id,
            Project.id == project_id
        )

        await self.__db.execute(query)
        await self.__db.flush()


    



