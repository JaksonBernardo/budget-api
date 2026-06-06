from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, delete, update, insert
from sqlalchemy.orm import selectinload
from api.models import Project, ProjectService



class ProjectServiceRepository:

    def __init__(self, db: AsyncSession) -> None:

        self.__db = db

    async def save(self, list_project_service: List[Dict[str, Any]]) -> None:

        query = insert(ProjectService)

        await self.__db.execute(
            query, list_project_service
        )

        await self.__db.flush()


    async def delete_by_project_id(self, project_id: int) -> None:

        query = delete(ProjectService).where(ProjectService.project_id == project_id)

        await self.__db.execute(query)
        await self.__db.flush()




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
            selectinload(Project.services)
        ).execution_options(populate_existing = True)

        result = await self.__db.execute(query)

        return result.scalar_one_or_none()


    



