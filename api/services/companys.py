from typing import List, Optional, Dict
from datetime import datetime, timedelta
import pytz

from api.models import Company, Subscription
from api.repositories import (
    CompanyRepository,
    PlanRepository,
    SubscriptionRepository
)
from api.schemas import (
    CompanySchema
)
from api.asaas.Asaas import (
    AsaasCustomers,
    AsaasSubscriptions
)
from api.exceptions import (
    CompanyNotFound,
    NameAlreadyExists,
    CnpjAlreadyExists,
    PlanNotFound
)

class CompanyService:

    def __init__(
        self,
        company_repository: CompanyRepository,
        plan_repository: PlanRepository,
        subscription_repository: SubscriptionRepository
    ):
        self.__company_repository = company_repository
        self.__plan_repository = plan_repository
        self.__subscription_repository = subscription_repository
    
    async def create(
        self, 
        company_schema: CompanySchema, 
        asaas_customers: AsaasCustomers,
        asaas_subscriptions: AsaasSubscriptions
    ) -> Company:

        plan = await self.__plan_repository.get_by_id(company_schema.plan_id)

        if not plan:

            raise PlanNotFound()
        
        company = await self.__company_repository.get_by_name(
            company_schema.name
        )

        if company:

            raise NameAlreadyExists()
        
        company = await self.__company_repository.get_by_document(
            company_schema.cnpj
        )

        if company:

            raise CnpjAlreadyExists()

        _BRAZIL_TIMEZONE_ = pytz.timezone("America/Sao_Paulo")

        company_db = Company(
            customer_id = None,
            photo = company_schema.photo,
            email = company_schema.email,
            name = company_schema.name,
            address = company_schema.address,
            number = company_schema.number,
            state = company_schema.state,
            cep = company_schema.cep,
            city = company_schema.city,
            cnpj = company_schema.cnpj,
            phone = company_schema.phone,
            whatsapp = company_schema.whatsapp,
            website = company_schema.website,
            is_blocked = company_schema.is_blocked,
            plan_id = company_schema.plan_id,
            created_at = datetime.now(_BRAZIL_TIMEZONE_),
            updated_at = datetime.now(_BRAZIL_TIMEZONE_)
        )

        data_customer = {
            "name": company_schema.name,
            "cpfCnpj": company_schema.cnpj,
            "email": company_schema.email
        }

        new_customer = asaas_customers().post_customer(data_customer)

        customer_id = None

        if "id" in new_customer:

            customer_id = new_customer.get("id")
            company_db.customer_id = customer_id

        start_date = datetime.now(_BRAZIL_TIMEZONE_)
        end_date = start_date + timedelta(days = 365)

        data_subscription = {
            "customer": customer_id,
            "billingType": "UNDEFINED",
            "value": float(plan.price),
            "nextDueDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d"),
            "cycle": "MONTHLY",
            "description": plan.description if plan.description else None
        }

        response: Dict = asaas_subscriptions().post_subscription(data_subscription)

        company = await self.__company_repository.create(company_db)

        subscription_db = Subscription(
            subscription_id = response.get('id'),
            company_id = company.id,
            plan_id = company_schema.plan_id,
            billing_type = response.get('billingType'),
            cycle = response.get('cycle'),
            value = float(plan.price),
            start_date = start_date,
            end_date = end_date,
            description = plan.description if plan.description else None,
            status = response.get('status'),
            discount_value = 0.0,
            discount_type = "FIXED",
            created_at = datetime.now(_BRAZIL_TIMEZONE_),
            updated_at = datetime.now(_BRAZIL_TIMEZONE_)
        )

        subscription = await self.__subscription_repository.create(subscription_db)

        return company


    async def list(self, limit: int, offset: int, search: str | None) -> List[Company]:

        companys = await self.__company_repository.get_all(
            limit,
            offset,
            search
        )

        return companys
    

    async def get_by_id(self, company_id: int) -> Company | None:

        company = await self.__company_repository.get_by_id(company_id)

        if not company:

            raise CompanyNotFound()
        
        return company
    

    async def update_company(
        self, 
        company_data: Dict, 
        company_id: int, 
        asaas_customers: AsaasCustomers
    ) -> Company | None:
        
        company = await self.__company_repository.get_by_id(company_id)

        if not company:

            raise CompanyNotFound()
        
        if "name" in company_data and company_data["name"] != company.name:

            has_name = await self.__company_repository.get_by_name(
                company_data["name"]
            )

            if has_name:

                raise NameAlreadyExists()
            
            company.name = company_data["name"]
            
        if "cnpj" in company_data and company_data["cnpj"] != company.cnpj:

            has_document = await self.__company_repository.get_by_document(
                company_data["cnpj"]
            )

            if has_document:

                raise CnpjAlreadyExists()
            
            company.cnpj = company_data["cnpj"]
        
        old_plan = company.plan_id

        if "plan_id" in company_data and company_data["plan_id"] != company.plan_id:

            plan = await self.__plan_repository.get_by_id(
                company_data["plan_id"]
            )

            if not plan:

                raise PlanNotFound()
            
            company.plan_id = company_data["plan_id"]

        

        
    async def delete_company(
        self, company_id: int, asaas_customers: AsaasCustomers
    ) -> None:
        
        pass


