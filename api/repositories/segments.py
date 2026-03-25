from sqlalchemy.ext.asyncio import AsyncSession

from api.models import Segment


class SegmentRepository:

    def __init__(self, db: AsyncSession):

        self.__db = db

    
    async def save(self, segment: Segment) -> Segment:

        self.__db.add(segment)
        await self.__db.commit()
        await self.__db.refresh(segment)

        return segment
    
    

