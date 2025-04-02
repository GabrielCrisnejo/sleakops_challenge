from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from src import models, schemas
from decimal import Decimal
from src.logger import setup_logger
from typing import List, Optional

logger = setup_logger("pricing_data_service")

class PricingDataService:
    def __init__(self, db: Session):
        self.db = db

    def get_pricing_data(self, database_engine: Optional[str] = None, instance_type: Optional[str] = None, vcpu: Optional[int] = None, memory: Optional[str] = None, limit: int = 10, offset: int = 0) -> List[schemas.SimplifiedPricingData]:
        try:
            query = self.db.query(models.PricingData).options(joinedload(models.PricingData.terms).joinedload(models.Term.price_dimensions))
            if database_engine:
                query = query.filter(models.PricingData.database_engine == database_engine)
            if instance_type:
                query = query.filter(models.PricingData.instance_type == instance_type)
            if vcpu:
                query = query.filter(models.PricingData.vcpu == vcpu)
            if memory:
                query = query.filter(models.PricingData.memory == memory)
            results = query.offset(offset).limit(limit).all()

            simplified_results = []
            for pricing_data in results:
                for term in pricing_data.terms:
                    database_price = []
                    for price_dimension in term.price_dimensions:
                        price_usd = Decimal(str(price_dimension.priceUSD)) if price_dimension.priceUSD else Decimal('0')
                        daily_price = price_usd
                        monthly_price = daily_price * 30
                        annual_price = daily_price * 365
                        database_price.append(schemas.DatabasePrice(rateCode=price_dimension.rateCode, dailyPrice=daily_price, monthlyPrice=monthly_price, annualPrice=annual_price))

                    simplified_data = schemas.SimplifiedPricingData(sku=pricing_data.sku, database_engine=pricing_data.database_engine, instance_type=pricing_data.instance_type, memory=pricing_data.memory, vcpu=pricing_data.vcpu, termType=term.termType, databasePrice=database_price)

                    if term.termType == "Reserved":
                        simplified_data.termAttributes = schemas.TermAttributes(LeaseContractLength=term.leaseContractLength, PurchaseOption=term.purchaseOption)

                    simplified_results.append(simplified_data)

            return simplified_results
        except Exception as e:
            logger.error(f"Error en get_pricing_data: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")