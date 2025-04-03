from sqlalchemy.orm import Session
from fastapi import HTTPException
from src import models, schemas
from src.logger import setup_logger

logger = setup_logger("term_service")

class TermService:
    def __init__(self, db: Session):
        self.db = db

    def create_term(self, sku: str, term: schemas.TermCreate):
        """Create a new term for the specified SKU"""
        pricing_data = self.db.query(models.PricingData).filter(models.PricingData.sku == sku).first()
        if not pricing_data:
            logger.error(f"SKU {sku} not found")
            raise HTTPException(status_code=404, detail="SKU not found")

        db_term = models.Term(sku=sku, **term.model_dump())
        self.db.add(db_term)
        self.db.commit()
        self.db.refresh(db_term)
        logger.info(f"Term created with ID: {db_term.id}")
        return db_term

    def update_term(self, sku: str, term_type: str, term: schemas.TermCreate):
        """Update an existing term for the specified SKU and term type"""
        db_term = self.db.query(models.Term).filter(
            models.Term.sku == sku,
            models.Term.termType == term_type
        ).first()
        
        if not db_term:
            raise HTTPException(status_code=404, detail="Term not found")

        for key, value in term.model_dump().items():
            setattr(db_term, key, value)
            
        self.db.commit()
        self.db.refresh(db_term)
        logger.info(f"Term {db_term.id} updated successfully")
        return db_term

    def delete_term(self, sku: str, term_type: str):
        """Delete a term for the specified SKU and term type"""
        db_term = self.db.query(models.Term).filter(
            models.Term.sku == sku,
            models.Term.termType == term_type
        ).first()
        
        if not db_term:
            raise HTTPException(status_code=404, detail="Term not found")

        # Remove term reference from pricing data if exists
        pricing_data = self.db.query(models.PricingData).filter(
            models.PricingData.sku == sku
        ).first()
        
        if pricing_data:
            pricing_data.terms = [term for term in pricing_data.terms if term.id != db_term.id]
            self.db.add(pricing_data)
            self.db.commit()

        self.db.delete(db_term)
        self.db.commit()
        logger.info(f"Term {db_term.id} deleted successfully")
        return {"status": "success", "message": "Term deleted successfully"}