from fastapi import APIRouter, Depends, HTTPException
from . import models, schemas
from sqlalchemy.orm import Session, joinedload
from src.database_manager import DatabaseManager
from typing import List, Optional
from src.logger import setup_logger
from decimal import Decimal

logger = setup_logger("routes")

router = APIRouter()

@router.get("/pricing_data/", response_model=List[schemas.SimplifiedPricingData])
def read_pricing_data(db: Session = Depends(DatabaseManager().get_db), database_engine: Optional[str] = None, instance_type: Optional[str] = None, vcpu: Optional[int] = None, memory: Optional[str] = None):
    try:
        query = db.query(models.PricingData).options(
            joinedload(models.PricingData.terms).joinedload(models.Term.price_dimensions)
        )
        if database_engine:
            query = query.filter(models.PricingData.database_engine == database_engine)
        if instance_type:
            query = query.filter(models.PricingData.instance_type == instance_type)
        if vcpu:
            query = query.filter(models.PricingData.vcpu == vcpu)
        if memory:
            query = query.filter(models.PricingData.memory == memory)
        results = query.all()

        simplified_results = []
        for pricing_data in results:
            for term in pricing_data.terms:
                database_price = []
                for price_dimension in term.price_dimensions:
                    price_usd = Decimal(str(price_dimension.priceUSD)) if price_dimension.priceUSD else Decimal('0')
                    daily_price = price_usd * 24
                    monthly_price = daily_price * 30
                    annual_price = daily_price * 365
                    database_price.append(schemas.DatabasePrice(
                        rateCode=price_dimension.rateCode,
                        dailyPrice=daily_price,
                        monthlyPrice=monthly_price,
                        annualPrice=annual_price
                    ))

                simplified_data = schemas.SimplifiedPricingData(
                    sku=pricing_data.sku,
                    database_engine=pricing_data.database_engine,
                    instance_type=pricing_data.instance_type,
                    memory=pricing_data.memory,
                    vcpu=pricing_data.vcpu,
                    termType=term.termType,
                    databasePrice=database_price
                )

                # Agregar termAttributes solo si termType es "Reserved"
                if term.termType == "Reserved":
                    simplified_data.termAttributes = schemas.TermAttributes(
                        LeaseContractLength=term.leaseContractLength,
                        PurchaseOption=term.purchaseOption,
                    )

                simplified_results.append(simplified_data)

        return simplified_results
    except Exception as e:
        logger.error(f"Error en read_pricing_data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/terms/", response_model=schemas.Term)
def create_term(term: schemas.TermCreate, db: Session = Depends(DatabaseManager().get_db)):
    db_term = models.Term(sku=term.sku, **term.dict(exclude={"price_dimensions"}))
    db.add(db_term)
    db.commit()
    db.refresh(db_term)
    for price_dimension in term.price_dimensions:
        db_price_dimension = models.PriceDimensions(term_id=db_term.id, **price_dimension.dict())
        db.add(db_price_dimension)
        db.commit()
        db.refresh(db_price_dimension)
    return db_term

@router.put("/terms/{term_id}", response_model=schemas.Term)
def update_term(term_id: int, term: schemas.TermCreate, db: Session = Depends(DatabaseManager().get_db)):
    db_term = db.query(models.Term).filter(models.Term.id == term_id).first()
    if not db_term:
        raise HTTPException(status_code=404, detail="Term not found")
    for key, value in term.dict(exclude={"price_dimensions"}).items():
        setattr(db_term, key, value)
    db.commit()
    db.refresh(db_term)
    # Actualizar price_dimensions (lógica adicional necesaria)
    return db_term

@router.delete("/terms/{term_id}", response_model=dict)
def delete_term(term_id: int, db: Session = Depends(DatabaseManager().get_db)):
    db_term = db.query(models.Term).filter(models.Term.id == term_id).first()
    if not db_term:
        raise HTTPException(status_code=404, detail="Term not found")
    db.delete(db_term)
    db.commit()
    return {"message": "Term deleted successfully"}