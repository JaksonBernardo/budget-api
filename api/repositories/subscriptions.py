from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from api.models import Subscription

class SubscriptionRepository:

    def __init__(self, db: AsyncSession):

        self.__db = db

    async def create(self, subscription: Subscription) -> Subscription:

        self.__db.add(subscription)
        await self.__db.flush()
        await self.__db.refresh(subscription)

        return subscription
    
