from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database_manager import DatabaseManager
from src.services.pricing_data_service import PricingDataService
from src.services.term_service import TermService
from . import schemas

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Welcome to the SleakOps Challenge API!"}

@router.get("/pricing_data/", response_model=list[schemas.SimplifiedPricingData])
def read_pricing_data(db: Session = Depends(DatabaseManager().get_db), database_engine: str | None = None, instance_type: str | None = None, vcpu: int | None = None, memory: str | None = None, limit: int = 10, offset: int = 0):
    return PricingDataService(db).get_pricing_data(database_engine, instance_type, vcpu, memory, limit, offset)

@router.post("/skus/{sku}/terms/", response_model=schemas.Term)
def create_term_by_sku(sku: str, term: schemas.TermCreate, db: Session = Depends(DatabaseManager().get_db)):
    return TermService(db).create_term(sku, term)

@router.put("/skus/{sku}/terms/{term_type}", response_model=schemas.Term)
def update_term_by_sku(sku: str, term_type: str, term: schemas.TermCreate, db: Session = Depends(DatabaseManager().get_db)):
    return TermService(db).update_term(sku, term_type, term)

@router.delete("/skus/{sku}/terms/{term_type}", response_model=dict)
def delete_term_by_sku(sku: str, term_type: str, db: Session = Depends(DatabaseManager().get_db)):
    return TermService(db).delete_term(sku, term_type)