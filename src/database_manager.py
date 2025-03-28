import os
import threading
from typing import Any, Optional, List, Tuple
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session as SQLAlchemySession
from src.logger import setup_logger
from src.config import DB_URL

# Logger configuration
logger = setup_logger("Database")

# Database connection setup
engine = create_engine(DB_URL, echo=False, pool_pre_ping=True)
Session = sessionmaker(bind=engine)

class DatabaseManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """Ensures a single instance of DatabaseManager (Singleton Pattern)."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-check locking
                    cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def get_db(self):
        """Yields a database session to be used as a dependency."""
        session = Session()
        try:
            yield session
        finally:
            session.close()

    def execute_query(self, query: str) -> Optional[List[Tuple]]:
        """Executes a SQL query and returns the results."""
        with self.get_db() as db:
            try:
                result = db.execute(text(query))
                return result.fetchall()
            except Exception as e:
                logger.error(f"Error executing query: {e}")
                return None

    def execute_sql_file(self, file_path: str) -> None:
        """Executes SQL statements from a file."""
        if not os.path.exists(file_path):
            logger.warning(f"SQL file {file_path} not found.")
            return

        with self.get_db() as db:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    sql_commands = file.read()
                    db.execute(text(sql_commands))
                    db.commit()
                logger.info(f"Executed {file_path} successfully.")
            except Exception as e:
                db.rollback()
                logger.error(f"Error executing {file_path}: {e}")

    def insert_pricing_data(self, sku: str, product_family: str, database_engine: str, instance_type: str, memory: str, vcpu: int) -> None:
        """Inserts AWS RDS pricing data into the database."""
        with self.get_db() as db:
            try:
                query = text("""
                    INSERT INTO pricing_data (sku, product_family, database_engine, instance_type, memory, vcpu)
                    VALUES (:sku, :product_family, :database_engine, :instance_type, :memory, :vcpu)
                    ON CONFLICT (sku) DO NOTHING
                """)
                db.execute(query, {
                    "sku": sku,
                    "product_family": product_family,
                    "database_engine": database_engine,
                    "instance_type": instance_type,
                    "memory": memory,
                    "vcpu": vcpu
                })
                db.commit()
                logger.info(f"Inserted pricing data for {sku}.")
            except Exception as e:
                db.rollback()
                logger.error(f"Error inserting pricing data: {e}")

    def insert_term_data(self, sku, offer_term_code, effective_date, term_type, lease_contract_length, purchase_option):
        with self.get_db() as db:
            query = text("""
                INSERT INTO terms (sku, offerTermCode, effectiveDate, termType, leaseContractLength, purchaseOption)
                VALUES (:sku, :offer_term_code, :effective_date, :term_type, :lease_contract_length, :purchase_option)
                RETURNING id
            """)
            result = db.execute(query, {
                "sku": sku,
                "offer_term_code": offer_term_code,
                "effective_date": effective_date,
                "term_type": term_type,
                "lease_contract_length": lease_contract_length,
                "purchase_option": purchase_option
            })
            term_id = result.fetchone()[0]
            db.commit()
            return term_id

    def insert_price_dimension(self, term_id, rate_code, unit, begin_range, end_range, description, price_usd):
        with self.get_db() as db:
            query = text("""
                INSERT INTO price_dimensions (term_id, rateCode, unit, beginRange, endRange, description, priceUSD)
                VALUES (:term_id, :rate_code, :unit, :begin_range, :end_range, :description, :price_usd)
            """)
            db.execute(query, {
                "term_id": term_id,
                "rate_code": rate_code,
                "unit": unit,
                "begin_range": begin_range,
                "end_range": end_range,
                "description": description,
                "price_usd": price_usd
            })
            db.commit()