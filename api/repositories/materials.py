from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, delete

from api.models import Material


class MaterialRepository:

    def __init__(self, db: AsyncSession):

        self.__db = db


    async def save(self, material: Material) -> Material:

        self.__db.add(material)
        await self.__db.commit()
        await self.__db.refresh(material)

        return material
    
    


