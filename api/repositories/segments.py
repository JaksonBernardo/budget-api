from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.models import Segment

class SegmentRepository:

    def __init__(self, db: AsyncSession):

        self.__db = db

    
    async def save(self, segment: Segment) -> Segment:

        self.__db.add(segment)
        await self.__db.commit()
        await self.__db.refresh(segment)

        return segment
    
    async def get_by_company_id(self, company_id: int) -> List[Segment]:

        segments = await self.__db.execute(
            select(Segment).where(Segment.company_id == company_id)
        )

        return segments.scalars().all()
    


