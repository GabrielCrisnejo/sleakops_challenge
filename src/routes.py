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
                    daily_price = price_usd
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

@router.post("/skus/{sku}/terms/", response_model=schemas.Term)
def create_term_by_sku(sku: str, term: schemas.TermCreate, db: Session = Depends(DatabaseManager().get_db)):
    """Crea un término para un SKU específico."""
    logger.info(f"Intentando crear término para SKU: {sku}")
    pricing_data = db.query(models.PricingData).filter(models.PricingData.sku == sku).first()
    if not pricing_data:
        logger.error(f"SKU {sku} no encontrado")
        raise HTTPException(status_code=404, detail="SKU not found")

    # Si necesitas offerTermCode y effectiveDate, agrégalos aquí
    db_term = models.Term(sku=sku, **term.dict())
    db.add(db_term)
    db.commit()
    db.refresh(db_term)
    logger.info(f"Término creado con ID: {db_term.id}")

    return db_term

@router.put("/skus/{sku}/terms/{term_type}", response_model=schemas.Term)
def update_term_by_sku(sku: str, term_type: str, term: schemas.TermCreate, db: Session = Depends(DatabaseManager().get_db)):
    """Actualiza un término para un SKU específico y term_type."""
    db_term = db.query(models.Term).filter(models.Term.sku == sku, models.Term.termType == term_type).first()
    if not db_term:
        raise HTTPException(status_code=404, detail="Term not found")

    for key, value in term.dict().items():
        setattr(db_term, key, value)
    db.commit()
    db.refresh(db_term)

    return db_term

@router.delete("/skus/{sku}/terms/{term_type}", response_model=dict)
def delete_term_by_sku(sku: str, term_type: str, db: Session = Depends(DatabaseManager().get_db)):
    """Elimina un término para un SKU específico y term_type."""
    db_term = db.query(models.Term).filter(models.Term.sku == sku, models.Term.termType == term_type).first()
    if not db_term:
        raise HTTPException(status_code=404, detail="Term not found")

    # Eliminar la relación con PricingData
    pricing_data = db.query(models.PricingData).filter(models.PricingData.sku == sku).first()
    if pricing_data:
        pricing_data.terms = [term for term in pricing_data.terms if term.id != db_term.id]
        db.add(pricing_data)
        db.commit()  # Agrega este commit para confirmar los cambios en pricing_data

    db.delete(db_term)
    db.commit()  # Confirma la eliminación del término

    return {"message": "Term deleted successfully"}
