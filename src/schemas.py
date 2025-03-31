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
    termAttributes: Optional[TermAttributes] = None
    databasePrice: list[DatabasePrice]

class PriceDimension(BaseModel):
    rateCode: str
    unit: str
    beginRange: Optional[Decimal] = None
    endRange: Optional[str] = None
    description: str
    priceUSD: Optional[Decimal] = None

class TermCreate(BaseModel):
    termType: str
    leaseContractLength: Optional[str] = None
    purchaseOption: Optional[str] = None

class Term(BaseModel):
    termType: str
    leaseContractLength: Optional[str] = None
    purchaseOption: Optional[str] = None