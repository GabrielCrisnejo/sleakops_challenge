from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal
from datetime import datetime

class TermAttributes(BaseModel):
    LeaseContractLength: Optional[str] = None
    PurchaseOption: Optional[str] = None

class DatabasePrice(BaseModel):
    rateCode: Optional[str] = None
    dailyPrice: Optional[Decimal] = None
    monthlyPrice: Optional[Decimal] = None
    annualPrice: Optional[Decimal] = None

class SimplifiedPricingData(BaseModel):
    sku: str
    database_engine: Optional[str] = None
    instance_type: Optional[str] = None
    memory: Optional[str] = None
    vcpu: Optional[int] = None
    termType: str
    termAttributes: Optional[TermAttributes] = None # Agregado
    databasePrice: list[DatabasePrice]

class PriceDimensionBase(BaseModel):
    rateCode: str
    unit: str
    beginRange: Optional[Decimal] = None
    endRange: Optional[str] = None
    description: str
    priceUSD: Optional[Decimal] = None

class PriceDimensionCreate(PriceDimensionBase):
    pass

class PriceDimension(PriceDimensionBase):
    id: int
    term_id: int

    class Config:
        from_attributes = True

class TermBase(BaseModel):
    offerTermCode: str
    effectiveDate: datetime
    termType: str
    leaseContractLength: Optional[str] = None
    purchaseOption: Optional[str] = None

class TermCreate(TermBase):
    price_dimensions: List[PriceDimensionCreate]

class Term(TermBase):
    id: int
    sku: str
    price_dimensions: List[PriceDimension]

    class Config:
        from_attributes = True

class PricingDataBase(BaseModel):
    sku: str
    product_family: Optional[str] = None
    database_engine: Optional[str] = None
    instance_type: Optional[str] = None
    memory: Optional[str] = None
    vcpu: Optional[int] = None

class PricingDataCreate(PricingDataBase):
    terms: List[TermCreate]

class PricingData(PricingDataBase):
    id: int
    terms: List[Term]

    class Config:
        from_attributes = True