import pytz
from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import (
    Service, 
    ServiceEmployee, 
    ServiceMaterial, 
    ServicePrice
)
from api.repositories import (
    MaterialRepository,
    SegmentRepository,
    EmployeeRepository,
    PriceRepository,
    CompanyRepository,
    PrecificationServiceRepository,
    ServicePriceRepository,
    ServiceMaterialRepository,
    ServiceEmployeeRepository
)
from api.schemas import (
    ServiceSchema,
    ServicePriceSchema,
    ServicePublicSchema,
    ServiceEmployeeSchema,
    ServiceMaterialSchema,
    ServiceEmployeeSchema,
    ServicePublicPriceSchema,
    ServicePublicEmployeeSchema,
    ServicePublicMaterialSchema,
    ServiceUpdateSchema,
)
from api.exceptions import (
    CompanyNotFound,
    SegmentNotFound,
    MaterialNotFound,
    EmployeeNotFound,
    PriceNotFound,
    PriceExceedValue,
    ServiceNotFound,
    ServiceInvalidName,
    ServiceAccesDenied
)


class PrecificationService:

    def __init__(
        self,
        segment_repository: SegmentRepository,
        material_repository: MaterialRepository,
        employee_repository: EmployeeRepository,
        price_repository: PriceRepository,
        precification_repository: PrecificationServiceRepository,
        service_material_repository: ServiceMaterialRepository,
        service_employee_repository: ServiceEmployeeRepository,
        service_price_repository: ServicePriceRepository,
        company_repository: CompanyRepository,
        db: AsyncSession
    ) -> None:
        
        self.__segment_repository = segment_repository
        self.__material_repository = material_repository
        self.__employee_repository = employee_repository
        self.__price_repository = price_repository
        self.__precification_repository = precification_repository
        self.__service_material_repository = service_material_repository
        self.__service_employee_repository = service_employee_repository
        self.__service_price_repository = service_price_repository
        self.__company_repository = company_repository
        self.__db = db

    async def create(self, service_data: ServiceSchema) -> Service:

        try:
            company = await self.__company_repository.get_by_id(
                service_data.company_id
            )

            if not company: raise CompanyNotFound()

            segment = await self.__segment_repository.get_by_id(
                service_data.company_id,
                service_data.segment_id
            )

            if not segment: raise SegmentNotFound()

            if service_data.name:

                if not service_data.name.strip():

                    raise ServiceInvalidName()

                service = await self.__precification_repository.get_by_name(
                    service_data.company_id, service_data.name.strip()
                )

                if service:

                    raise ServiceAccesDenied("Ja existe um servico com esse nome")

            materials_rows = []
            employees_rows = []
            prices_rows = []

            if service_data.materials:

                material_ids = {
                    item.material_id
                    for item in service_data.materials
                }

                materials = await self.__material_repository.get_by_ids(
                    service_data.company_id,
                    list(material_ids)
                )

                if len(materials) != len(material_ids):
                    raise MaterialNotFound()

                materials_map = {m.id: m for m in materials}

                for item in service_data.materials:
                    material = materials_map[item.material_id]

                    materials_rows.append({
                        "material_id": material.id,
                        "qtd_material": item.qtd_material,
                        "total_cost": material.unit_cost * item.qtd_material
                    })

            if service_data.employees:

                employee_ids = {
                    item.employee_id
                    for item in service_data.employees
                }

                employees = await self.__employee_repository.get_by_ids(
                    service_data.company_id,
                    list(employee_ids)
                )

                if len(employees) != len(employee_ids):
                    raise EmployeeNotFound()

                employees_map = {e.id: e for e in employees}

                for item in service_data.employees:
                    employee = employees_map[item.employee_id]

                    employees_rows.append({
                        "employee_id": employee.id,
                        "minute_works": item.minute_works,
                        "total_cost": employee.cost_per_minute * item.minute_works
                    })

            if service_data.prices:

                price_ids = {
                    item.price_id
                    for item in service_data.prices
                }

                prices = await self.__price_repository.get_by_ids(
                    service_data.company_id,
                    list(price_ids)
                )

                if len(prices) != len(price_ids):
                    raise PriceNotFound()

                prices_map = {p.id: p for p in prices}

                total_base_cost = (
                    sum(row["total_cost"] for row in materials_rows) +
                    sum(row["total_cost"] for row in employees_rows)
                )

                for item in service_data.prices:

                    price = prices_map[item.price_id]

                    total_rates = (
                        item.fixed_expenses +
                        item.impost +
                        item.commission +
                        item.others_rates +
                        item.profit_margin
                    )

                    if total_rates >= 100: 
                        
                        raise PriceExceedValue()

                    markup = 100 / (100 - total_rates)
                    value = total_base_cost * markup

                    prices_rows.append({
                        "price_id": price.id,
                        "fixed_expenses": item.fixed_expenses,
                        "impost": item.impost,
                        "commission": item.commission,
                        "others_rates": item.others_rates,
                        "profit_margin": item.profit_margin,
                        "markup": markup,
                        "value": value
                    })

            service_entity = Service(
                name=service_data.name,
                segment_id=service_data.segment_id,
                description=service_data.description,
                company_id=service_data.company_id
            )

            service = await self.__precification_repository.save(service_entity)

            for row in materials_rows:
                row["service_id"] = service.id

            for row in employees_rows:
                row["service_id"] = service.id

            for row in prices_rows:
                row["service_id"] = service.id

            if materials_rows:
                await self.__service_material_repository.save(materials_rows)

            if employees_rows:
                await self.__service_employee_repository.save(employees_rows)

            if prices_rows:
                await self.__service_price_repository.save(prices_rows)

            await self.__db.commit()

            return await self.__precification_repository.get_by_id(service.company_id, service.id)

        except Exception as e:
            await self.__db.rollback()
            raise e

    async def update(self, service_id: int, service_data: ServiceUpdateSchema) -> Service:

        try:
            company = await self.__company_repository.get_by_id(service_data.company_id)
            if not company: raise CompanyNotFound()

            existing_service = await self.__precification_repository.get_by_id(
                service_data.company_id, service_id
            )
            if not existing_service: raise ServiceNotFound()

            if service_data.name:
                if not service_data.name.strip():
                    raise ServiceInvalidName()

                service_with_name = await self.__precification_repository.get_by_name(
                    service_data.company_id, service_data.name.strip()
                )

                if service_with_name and service_with_name.id != service_id:
                    raise ServiceAccesDenied("Ja existe um servico com esse nome")
                
                existing_service.name = service_data.name.strip()

            if service_data.segment_id:
                segment = await self.__segment_repository.get_by_id(
                    service_data.company_id, service_data.segment_id
                )
                if not segment: raise SegmentNotFound()
                existing_service.segment_id = service_data.segment_id

            if service_data.description is not None:
                existing_service.description = service_data.description

            materials_rows = []
            employees_rows = []
            prices_rows = []

            if service_data.materials is not None:
                material_ids = {item.material_id for item in service_data.materials}
                if material_ids:
                    materials = await self.__material_repository.get_by_ids(
                        service_data.company_id, list(material_ids)
                    )
                    if len(materials) != len(material_ids):
                        raise MaterialNotFound()

                    materials_map = {m.id: m for m in materials}
                    for item in service_data.materials:
                        material = materials_map[item.material_id]
                        materials_rows.append({
                            "service_id": service_id,
                            "material_id": material.id,
                            "qtd_material": item.qtd_material,
                            "total_cost": material.unit_cost * item.qtd_material
                        })

            if service_data.employees is not None:
                employee_ids = {item.employee_id for item in service_data.employees}
                if employee_ids:
                    employees = await self.__employee_repository.get_by_ids(
                        service_data.company_id, list(employee_ids)
                    )
                    if len(employees) != len(employee_ids):
                        raise EmployeeNotFound()

                    employees_map = {e.id: e for e in employees}
                    for item in service_data.employees:
                        employee = employees_map[item.employee_id]
                        employees_rows.append({
                            "service_id": service_id,
                            "employee_id": employee.id,
                            "minute_works": item.minute_works,
                            "total_cost": employee.cost_per_minute * item.minute_works
                        })

            if service_data.prices is not None:
                price_ids = {item.price_id for item in service_data.prices}
                if price_ids:
                    prices = await self.__price_repository.get_by_ids(
                        service_data.company_id, list(price_ids)
                    )
                    if len(prices) != len(price_ids):
                        raise PriceNotFound()

                    prices_map = {p.id: p for p in prices}
                    
                    if service_data.materials is None or service_data.employees is None:
                        current_service = await self.__precification_repository.get_by_id(
                            service_data.company_id, service_id
                        )
                        
                        if service_data.materials is None:
                            for m in current_service.materials:
                                materials_rows.append({
                                    "total_cost": m.total_cost
                                })
                        
                        if service_data.employees is None:
                            for e in current_service.employees:
                                employees_rows.append({
                                    "total_cost": e.total_cost
                                })

                    total_base_cost = (
                        sum(row["total_cost"] for row in materials_rows) +
                        sum(row["total_cost"] for row in employees_rows)
                    )

                    if service_data.materials is None:
                        materials_rows = []
                    if service_data.employees is None:
                        employees_rows = []

                    for item in service_data.prices:
                        price = prices_map[item.price_id]
                        total_rates = (
                            item.fixed_expenses + item.impost +
                            item.commission + item.others_rates +
                            item.profit_margin
                        )

                        if total_rates >= 100: raise PriceExceedValue()

                        markup = 100 / (100 - total_rates)
                        value = total_base_cost * markup

                        prices_rows.append({
                            "service_id": service_id,
                            "price_id": price.id,
                            "fixed_expenses": item.fixed_expenses,
                            "impost": item.impost,
                            "commission": item.commission,
                            "others_rates": item.others_rates,
                            "profit_margin": item.profit_margin,
                            "markup": markup,
                            "value": value
                        })

            await self.__precification_repository.update(existing_service)

            if service_data.materials is not None:
                await self.__service_material_repository.delete_by_service_id(service_id)
                if materials_rows:
                    await self.__service_material_repository.save(materials_rows)

            if service_data.employees is not None:
                await self.__service_employee_repository.delete_by_service_id(service_id)
                if employees_rows:
                    await self.__service_employee_repository.save(employees_rows)

            if service_data.prices is not None:
                await self.__service_price_repository.delete_by_service_id(service_id)
                if prices_rows:
                    await self.__service_price_repository.save(prices_rows)

            await self.__db.commit()
            return await self.__precification_repository.get_by_id(service_data.company_id, service_id)

        except Exception as e:
            await self.__db.rollback()
            raise e

    async def list(
        self, company_id: int, limit: int, offset: int, search: str | None
    ) -> List[Service]:
        
        company = await self.__company_repository.get_by_id(company_id)

        if not company:

            raise CompanyNotFound()
        
        services = await self.__precification_repository.get_by_company_id(
            company_id, limit, offset, search
        )

        return services

    async def get(self, company_id: int, service_id: int) -> Service:

        company = await self.__company_repository.get_by_id(company_id)

        if not company:

            raise CompanyNotFound()
        
        service = await self.__precification_repository.get_by_id(
            company_id, service_id
        )

        if not service:

            raise ServiceNotFound()
        
        return service

    async def delete(self, company_id: int, service_id: int) -> None:

        company = await self.__company_repository.get_by_id(company_id)

        if not company:

            raise CompanyNotFound()
        
        service = await self.__precification_repository.get_by_id(
            company_id, service_id
        )

        if not service:

            raise ServiceNotFound()
        
        # E PRECISO FAZER UMA VERIFICACAO POSTERIORMENTE QUE NAO PODE DELETAR UM SERVICO QUE ESTA ATRELADO A ALGUM ORCAMENTO
        # TAMBEM NAO DELETAR SE FOR VENDA, CONSEQUENTEMENTE TERA REGISTROS FINANCEIROS RELACIONADOS A ELE

        # IDEIA DE DISPONIBILIZAR LINKS PUBLICOS PARA CLIENTES VEREM A PROPOSTA SER BAIXAR NADA NO CELULAR
        
        await self.__precification_repository.delete(company_id, service_id)




