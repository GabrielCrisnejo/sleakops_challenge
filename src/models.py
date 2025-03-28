from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class PricingData(Base):
    __tablename__ = "pricing_data"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, nullable=False)
    product_family = Column(String)
    database_engine = Column(String)
    instance_type = Column(String)
    memory = Column(String)
    vcpu = Column(Integer)

    terms = relationship("Term", back_populates="pricing_data")

class Term(Base):
    __tablename__ = "terms"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, ForeignKey("pricing_data.sku"))
    offerTermCode = Column(String)
    effectiveDate = Column(TIMESTAMP)
    termType = Column(String)
    leaseContractLength = Column(String)
    purchaseOption = Column(String)

    pricing_data = relationship("PricingData", back_populates="terms")
    price_dimensions = relationship("PriceDimension", back_populates="term")

class PriceDimension(Base):
    __tablename__ = "price_dimensions"

    id = Column(Integer, primary_key=True, index=True)
    term_id = Column(Integer, ForeignKey("terms.id"))
    rateCode = Column(String)
    unit = Column(String)
    beginRange = Column(Numeric)
    endRange = Column(String)
    description = Column(String)
    priceUSD = Column(Numeric)

    term = relationship("Term", back_populates="price_dimensions")