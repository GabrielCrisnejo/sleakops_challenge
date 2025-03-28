from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from decimal import Decimal

class PriceDimensionBase(BaseModel):
    rateCode: str
    unit: str
    beginRange: Optional[Decimal] = None
    endRange: Optional[str] = None # Permitir None
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
        from_attributes = True # Cambio aquí

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
        from_attributes = True # Cambio aquí