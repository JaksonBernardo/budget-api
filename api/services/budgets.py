import pytz
import asyncio
from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import (
    Budget,
    BudgetService as BS
)
from api.repositories import (
    CompanyRepository,
    PrecificationServiceRepository,
    ClientRepository,
    UserRepository,
    BudgetRepository,
    BudgetServiceRepository
)
from api.schemas import (
    BudgetPublicSchema,
    BudgetSchema,
    BudgetServicesSchema
)
from api.exceptions import (
    CompanyNotFound,
    ServiceNotFound,
    ClientNotFound,
    UserNotFound,
    ServicePriceNotFound,
)



class BudgetService:

    def __init__(
        self,
        company_repository: CompanyRepository,
        precification_repository: PrecificationServiceRepository,
        client_repository: ClientRepository,
        user_repository: UserRepository,
        budget_repository: BudgetRepository,
        budget_service_repository: BudgetServiceRepository,
        db: AsyncSession
    ) -> None:
        
        self.__company_repository = company_repository
        self.__precification_repository = precification_repository
        self.__client_repository = client_repository
        self.__user_repository = user_repository
        self.__budget_repository = budget_repository
        self.__budget_service_repository = budget_service_repository
        self.__db = db

    async def create(self, budget_data: BudgetSchema) -> Budget:

        try:

            company, client, user = await asyncio.gather(
                self.__company_repository.get_by_id(budget_data.company_id),
                self.__client_repository.get_by_id(budget_data.client_id),
                self.__user_repository.get_by_id(budget_data.user_id),
                # VERIFICACAO PENDENTE PARA STATUS_ID
                # VERIFICACAO PENDENTE PARA FORMA DE PAGAMENTO
            )

            if not company: raise CompanyNotFound()
            
            if not client: raise ClientNotFound()
            
            if not user: raise UserNotFound()
            
            budget_service_rows = []

            if budget_data.services:

                service_ids = {
                    item.service_id
                    for item in budget_data.services
                }

                services = await self.__precification_repository.get_by_ids(
                    budget_data.company_id,
                    list(service_ids)
                )

                if len(services) != len(service_ids): raise ServiceNotFound()

                services_map = {s.id : s for s in services}

                for serv in budget_data.services:

                    service_entity = services_map[serv.service_id]

                    service_price_ids = {p.price_id for p in service_entity.prices}
                    
                    if serv.price_id not in service_price_ids:
                        raise ServicePriceNotFound()

                    budget_service_rows.append({
                        "service_id": service_entity.id,
                        "price_id": serv.price_id,
                        "qtd": serv.qtd,
                        "service_value": serv.service_value,
                        "total_value": serv.total_value
                    })

            _BRAZIL_TIMEZONE_ = pytz.timezone("America/Sao_Paulo")

            budget_entity = Budget(
                client_id = budget_data.client_id,
                user_id = budget_data.user_id,
                validity_date = budget_data.validity_date,
                date_acceptance = budget_data.date_acceptance,
                date_starter_services = budget_data.date_starter_services,
                status_id = budget_data.status_id,
                payment_option = budget_data.payment_option,
                type_discount = budget_data.type_discount,
                value_discount = budget_data.value_discount,
                company_id = budget_data.company_id,
                created_at = datetime.now(_BRAZIL_TIMEZONE_),
                updated_at = datetime.now(_BRAZIL_TIMEZONE_)
            )

            budget = await self.__budget_repository.save(budget_entity)

            for row in budget_service_rows:
                
                row["budget_id"] = budget.id

            if budget_service_rows:

                await self.__budget_service_repository.save(budget_service_rows)

            await self.__db.commit()

            return await self.__budget_repository.get_by_id(budget.company_id, budget.id)
        
        except Exception as ex:

            self.__db.rollback()

            raise ex



