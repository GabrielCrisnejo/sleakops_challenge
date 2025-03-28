from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from src.database_manager import DatabaseManager
from typing import List, Optional
from src.logger import setup_logger

logger = setup_logger("routes")

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Welcome to the Pricing API"}

@router.get("/pricing_data/", response_model=List[schemas.PricingData])
def read_pricing_data(db: Session = Depends(DatabaseManager().get_db), database_engine: Optional[str] = None, instance_type: Optional[str] = None, vcpu: Optional[int] = None, memory: Optional[str] = None):
    try:
        query = db.query(models.PricingData)
        if database_engine:
            query = query.filter(models.PricingData.database_engine == database_engine)
        if instance_type:
            query = query.filter(models.PricingData.instance_type == instance_type)
        if vcpu:
            query = query.filter(models.PricingData.vcpu == vcpu)
        if memory:
            query = query.filter(models.PricingData.memory == memory)
        return query.all()
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