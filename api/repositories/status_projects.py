from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, delete, update
from api.models import StatusProject



class StatusProjectRepository:


    def __init__(self, db: AsyncSession) -> None:

        self.__db = db


    async def save(self, status_project: StatusProject) -> StatusProject:

        self.__db.add(status_project)

        await self.__db.flush()
        await self.__db.refresh(status_project)

        return status_project


    async def get_by_id(self, company_id: int, status_id: int) -> StatusProject | None:

        query = select(StatusProject).where(
            StatusProject.company_id == company_id,
            StatusProject.id == status_id
        )

        result = await self.__db.execute(query)

        return result.scalar_one_or_none()
    
    async def get_by_company_id(self, company_id: int, offset: int, limit: int, search: Optional[str] = None) -> List[StatusProject]:
        
        query = select(StatusProject).where(
            StatusProject.company_id == company_id
        )

        if search:
            query = query.where(StatusProject.name.ilike(f"%{search}%"))

        query = query.offset(offset).limit(limit)
        
        result = await self.__db.execute(query)
        
        return list(result.scalars().all())

    async def get_is_completed_by_company_id(self, company_id: int, exclude_id: int | None = None) -> StatusProject | None:
        
        query = select(StatusProject).where(
            and_(
                StatusProject.company_id == company_id,
                StatusProject.is_completed == True
            )
        )
        
        if exclude_id:
            query = query.where(StatusProject.id != exclude_id)
            
        result = await self.__db.execute(query)
        
        return result.scalar_one_or_none()

    async def update(self, company_id: int, status_id: int, data: Dict[str, Any]) -> StatusProject:
        
        query = update(StatusProject).where(
            and_(
                StatusProject.company_id == company_id,
                StatusProject.id == status_id
            )
        ).values(**data).returning(StatusProject)
        
        result = await self.__db.execute(query)
        
        return result.scalar_one()

    async def delete(self, company_id: int, status_id: int) -> None:
        
        query = delete(StatusProject).where(
            and_(
                StatusProject.company_id == company_id,
                StatusProject.id == status_id
            )
        )
        
        await self.__db.execute(query)
