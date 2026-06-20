import pytz
import asyncio
from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import (
    Budget,
    BudgetService as BS,
    Project,
    ProjectOrigin,
    ProjectService,
    ProjectServiceMaterial
)
from api.repositories import (
    CompanyRepository,
    PrecificationServiceRepository,
    ClientRepository,
    UserRepository,
    BudgetRepository,
    BudgetServiceRepository,
    StatusBudgetRepository,
    PaymentConditionRepository,
    ProjectRepository,
    ProjectServiceRepository,
    ProjectServiceMaterialRepository
)
from api.schemas import (
    BudgetPublicSchema,
    BudgetSchema,
    BudgetUpdateSchema,
    BudgetServicesSchema,
    BudgetUpdateStatusSchema
)
from api.exceptions import (
    CompanyNotFound,
    ServiceNotFound,
    ClientNotFound,
    UserNotFound,
    ServicePriceNotFound,
    StatusBudgetNotFound,
    BudgetNotFound,
    PaymentConditionNotFound
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
        status_budget_repository: StatusBudgetRepository,
        payment_condition_repository: PaymentConditionRepository,
        project_repository: ProjectRepository,
        project_service_repository: ProjectServiceRepository,
        project_service_material_repository: ProjectServiceMaterialRepository,
        db: AsyncSession
    ) -> None:
        
        self.__company_repository = company_repository
        self.__precification_repository = precification_repository
        self.__client_repository = client_repository
        self.__user_repository = user_repository
        self.__budget_repository = budget_repository
        self.__budget_service_repository = budget_service_repository
        self.__status_budget_repository = status_budget_repository
        self.__payment_condition_repository = payment_condition_repository
        self.__project_repository = project_repository
        self.__project_service_repository = project_service_repository
        self.__project_service_material_repository = project_service_material_repository
        self.__db = db

    async def create(self, budget_data: BudgetSchema) -> Budget:

        try:

            company, client, user, status_budget, payment_condition = await asyncio.gather(
                self.__company_repository.get_by_id(budget_data.company_id),
                self.__client_repository.get_by_id(budget_data.client_id),
                self.__user_repository.get_by_id(budget_data.user_id),
                self.__status_budget_repository.get_by_id(budget_data.company_id, budget_data.status_id),
                self.__payment_condition_repository.get_by_id(budget_data.company_id, budget_data.payment_condition)
            )

            if not company: raise CompanyNotFound()
            
            if not client: raise ClientNotFound()
            
            if not user: raise UserNotFound()

            if not status_budget: raise StatusBudgetNotFound()

            if not payment_condition: raise PaymentConditionNotFound()
            
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
                        "total_value": serv.qtd * serv.service_value
                    })

            _BRAZIL_TIMEZONE_ = pytz.timezone("America/Sao_Paulo")

            budget_entity = Budget(
                client_id = budget_data.client_id,
                user_id = budget_data.user_id,
                validity_date = budget_data.validity_date,
                date_acceptance = budget_data.date_acceptance,
                date_starter_services = budget_data.date_starter_services,
                status_id = budget_data.status_id,
                payment_condition = budget_data.payment_condition,
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

            await self.__db.rollback()

            raise ex

    async def list(
        self,
        company_id: int,
        offset: int,
        limit: int,
        client_id: Optional[int] = None,
        user_id: Optional[int] = None,
        year: Optional[int] = datetime.now().year,
        month: Optional[int] = datetime.now().month
    ) -> List[Budget]:
        
        company = await self.__company_repository.get_by_id(company_id)

        if not company: raise CompanyNotFound()

        budgets = await self.__budget_repository.get_by_company_id(
            company_id,
            offset,
            limit,
            client_id,
            user_id,
            year,
            month
        )

        return budgets

    async def get(self, company_id: int, budget_id: int) -> Budget | None:

        company = await self.__company_repository.get_by_id(company_id)

        if not company: raise CompanyNotFound()

        budget = await self.__budget_repository.get_by_id(
            company_id, budget_id
        )

        if not budget: raise BudgetNotFound()

        return budget

    async def update(self, company_id: int, budget_id: int, budget_data: BudgetUpdateSchema) -> Budget:

        try:
            budget = await self.get(company_id, budget_id)

            if budget_data.client_id:
                client = await self.__client_repository.get_by_id(budget_data.client_id)
                if not client: raise ClientNotFound()

            if budget_data.user_id:
                user = await self.__user_repository.get_by_id(budget_data.user_id)
                if not user: raise UserNotFound()

            if budget_data.status_id:
                status_budget = await self.__status_budget_repository.get_by_id(budget_data.status_id)
                if not status_budget: raise StatusBudgetNotFound()

            if budget_data.payment_condition:
                payment_condition = await self.__payment_condition_repository.get_by_id(company_id, budget_data.payment_condition)
                if not payment_condition: raise PaymentConditionNotFound()

            update_data = budget_data.model_dump(exclude_unset=True, exclude={"services"})
            
            _BRAZIL_TIMEZONE_ = pytz.timezone("America/Sao_Paulo")
            update_data["updated_at"] = datetime.now(_BRAZIL_TIMEZONE_)

            if budget_data.services is not None:
                
                await self.__budget_service_repository.delete_by_budget_id(budget_id)

                if budget_data.services:

                    service_ids = {item.service_id for item in budget_data.services}
                    services = await self.__precification_repository.get_by_ids(company_id, list(service_ids))

                    if len(services) != len(service_ids): raise ServiceNotFound()

                    services_map = {s.id : s for s in services}
                    budget_service_rows = []

                    for serv in budget_data.services:
                        service_entity = services_map[serv.service_id]
                        service_price_ids = {p.price_id for p in service_entity.prices}
                        
                        if serv.price_id not in service_price_ids:
                            raise ServicePriceNotFound()

                        budget_service_rows.append({
                            "budget_id": budget_id,
                            "service_id": service_entity.id,
                            "price_id": serv.price_id,
                            "qtd": serv.qtd,
                            "service_value": serv.service_value,
                            "total_value": serv.qtd * serv.service_value
                        })
                    
                    await self.__budget_service_repository.save(budget_service_rows)

            updated_budget = await self.__budget_repository.update(company_id, budget_id, update_data)
            
            await self.__db.commit()
            return await self.__budget_repository.get_by_id(company_id, budget_id)

        except Exception as ex:
            await self.__db.rollback()
            raise ex

    async def delete(self, company_id: int, budget_id: int) -> None:

        try:
            await self.get(company_id, budget_id)
            
            await self.__budget_service_repository.delete_by_budget_id(budget_id)
            await self.__budget_repository.delete(company_id, budget_id)
            
            await self.__db.commit()

        except Exception as ex:
            await self.__db.rollback()
            raise ex

    async def update_status(
        self, 
        company_id: int, 
        budget_id: int, 
        status_data: BudgetUpdateStatusSchema,

    ) -> Budget | None:

        try:

            company, budget, status_budget = await asyncio.gather(
                self.__company_repository.get_by_id(company_id),
                self.__budget_repository.get_by_id(company_id, budget_id),
                self.__status_budget_repository.get_by_id(company_id, status_data.status_id)
            )

            if not company:
                raise CompanyNotFound()

            if not budget:
                raise BudgetNotFound()

            if not status_budget:
                raise StatusBudgetNotFound()

            _BRAZIL_TIMEZONE_ = pytz.timezone("America/Sao_Paulo")

            if status_budget.is_sale and not budget.status.is_sale:

                project = Project(
                    budget_id=budget.id,
                    client_id=budget.client_id,
                    code=f"PROJ-{datetime.now(_BRAZIL_TIMEZONE_).year}-{budget.id}",
                    origin=ProjectOrigin.BUDGET,
                    campaign=1,
                    company_id=budget.company_id,
                    status_id=None,
                    start_date=budget.date_starter_services if budget.date_starter_services else datetime.now(_BRAZIL_TIMEZONE_).date(),
                    estimated_end_date=None,
                    end_date=None,
                    notes=None,
                    created_at=datetime.now(_BRAZIL_TIMEZONE_),
                    updated_at=datetime.now(_BRAZIL_TIMEZONE_),
                )

                self.__db.add(project)
                await self.__db.flush()

                project_services = []
                project_services_materials_rows = []

                for budget_service in budget.services:

                    ps = ProjectService(
                        project_id=project.id,
                        service_id=budget_service.service_id,
                        service_name=budget_service.service.name,
                        service_qtd=budget_service.qtd,
                        service_value=budget_service.service_value,
                        service_total_value=budget_service.total_value,
                    )

                    project_services.append(ps)

                self.__db.add_all(project_services)

                await self.__db.flush()

                for ps, budget_service in zip(project_services, budget.services):

                    service = await self.__precification_repository.get_by_id(
                        budget.company_id,
                        budget_service.service_id
                    )

                    for serv_mat in service.materials:

                        project_services_materials_rows.append(
                            ProjectServiceMaterial(
                                project_service_id=ps.id,
                                material_id=serv_mat.material_id,
                                material_name=serv_mat.material.name,
                                quantity=serv_mat.qtd_material * budget_service.qtd,
                                unit_cost=serv_mat.material.unit_cost,
                                total_cost=serv_mat.qtd_material * serv_mat.material.unit_cost * budget_service.qtd,
                            )
                        )

                if project_services_materials_rows:
                    self.__db.add_all(project_services_materials_rows)
                    await self.__db.flush()

            elif not status_budget.is_sale and budget.status.is_sale:

                project = await self.__project_repository.get_by_budget_id(
                    company_id, budget_id
                )

                if project:
                    await self.__project_service_repository.delete_by_project_id(
                        project.id
                    )
                    await self.__project_repository.delete(company_id, project.id)

            await self.__budget_repository.update(
                company_id,
                budget_id,
                {"status_id": status_data.status_id},
            )

            await self.__db.commit()

            return await self.__budget_repository.get_by_id(company_id, budget_id)

        except Exception as ex:

            await self.__db.rollback()
            raise ex



