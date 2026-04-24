import pytz
from typing import Dict, List, Optional
from datetime import datetime
from api.models import Price
from api.repositories import (
    PriceRepository,
    CompanyRepository,
)
from api.schemas.prices import (
    PriceSchema,
    PricePublicSchema,
)
from api.exceptions import (
    CompanyNotFound
)
from api.exceptions.prices import (
    PriceNotFound
)

class PriceService:

    def __init__(
        self,
        price_repository: PriceRepository,
        company_repository: CompanyRepository
    ):
        self._price_repository = price_repository
        self._company_repository = company_repository

    async def create(self, price_data: PriceSchema) -> Price:
        company = await self._company_repository.get_by_id(
            price_data.company_id
        )

        if not company:
            raise CompanyNotFound()
        
        price_db = Price(
            name = price_data.name,
            fixed_expenses = price_data.fixed_expenses,
            impost = price_data.impost,
            commission = price_data.commission,
            others_rates = price_data.others_rates,
            profit_margin = price_data.profit_margin,
            markup = price_data.markup,
            company_id = price_data.company_id
        )

        new_price = await self._price_repository.save(
            price_db
        )

        return new_price

    async def list(
        self,
        company_id: int,
        offset: int = 0,
        limit: int = 20,
        name: Optional[str] = None
    ) -> List[Price]:
        company = await self._company_repository.get_by_id(company_id)

        if not company:
            raise CompanyNotFound()

        prices = await self._price_repository.get_by_company_id(
            company_id,
            offset,
            limit,
            name
        )

        return prices

    async def get(self, company_id: int, price_id: int) -> Price:
        company = await self._company_repository.get_by_id(company_id)

        if not company:
            raise CompanyNotFound()

        price = await self._price_repository.get_by_id(company_id, price_id)

        if not price:
            raise PriceNotFound()

        return price

    async def delete(self, company_id: int, price_id: int) -> None:
        company = await self._company_repository.get_by_id(company_id)

        if not company:
            raise CompanyNotFound()

        price = await self._price_repository.get_by_id(company_id, price_id)

        if not price:
            raise PriceNotFound()

        await self._price_repository.delete_by_id(company_id, price_id)

    async def update(self, company_id: int, price_id: int, price_data: Dict) -> Price:
        company = await self._company_repository.get_by_id(company_id)

        if not company:
            raise CompanyNotFound()

        price = await self._price_repository.get_by_id(
            company_id,
            price_id
        )

        if not price:
            raise PriceNotFound()

        _BRAZIL_TIMEZONE_ = pytz.timezone("America/Sao_Paulo")
        
        if "name" in price_data:
            price.name = price_data["name"]
        if "fixed_expenses" in price_data:
            price.fixed_expenses = price_data["fixed_expenses"]
        if "impost" in price_data:
            price.impost = price_data["impost"]
        if "commission" in price_data:
            price.commission = price_data["commission"]
        if "others_rates" in price_data:
            price.others_rates = price_data["others_rates"]
        if "profit_margin" in price_data:
            price.profit_margin = price_data["profit_margin"]
        if "markup" in price_data:
            price.markup = price_data["markup"]
            
        price.updated_at = datetime.now(_BRAZIL_TIMEZONE_)

        return await self._price_repository.update(price)
