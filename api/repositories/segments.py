from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, delete
from api.models import Segment

class SegmentRepository:

    def __init__(self, db: AsyncSession):

        self.__db = db

    
    async def save(self, segment: Segment) -> Segment:

        self.__db.add(segment)
        await self.__db.commit()
        await self.__db.refresh(segment)

        return segment
    
    async def get_by_company_id(self, company_id: int, offset: int, limit: int, search: str | None) -> List[Segment]:

        query = select(Segment)

        if search:

            query = query.where(
                Segment.name.ilike(search)
            )

        query = query.offset(offset).limit(limit)
        
        query = query.where(Segment.company_id == company_id)

        segments = await self.__db.execute(
            query
        )

        return segments.scalars().all()
    
    async def get_by_id(self, company_id: int, segment_id: int) -> Segment | None:

        segment = await self.__db.execute(
            select(Segment).where(
                and_(
                    Segment.company_id == company_id,
                    Segment.id == segment_id
                )
            )
        )

        return segment.scalar_one_or_none()
    
    async def delete_by_id(self, company_id: int, segment_id: int) -> None:

        try:
            await self.__db.execute(
                delete(Segment).where(
                    and_(
                        Segment.company_id == company_id,
                        Segment.id == segment_id
                    )
                )
            )
            await self.__db.commit()
        except Exception:
            await self.__db.rollback()
            raise

