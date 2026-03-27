from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, delete
from api.models import LegalEntity, Client

class ClientRepository:

    def __init__(self, db: AsyncSession):

        self.__db = db

    