import json
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import DB_URL, SQL_FILES, DATA
from src.models import Base, PricingData, Term, PriceDimension

# Configuración de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RdsPricingDataLoader:
    def __init__(self, sql_dir, data_dir):
        self.sql_dir = sql_dir
        self.data_dir = data_dir
        self.engine = create_engine(DB_URL)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def process_json_files(self):
        """Procesa los archivos JSON y carga los datos en la base de datos."""
        try:
            json_files = [f for f in os.listdir(self.data_dir) if f.endswith(".json")]

            for file_name in json_files:
                file_path = os.path.join(self.data_dir, file_name)
                logger.info(f"Procesando archivo: {file_name}")

                with open(file_path, "r") as f:
                    data = json.load(f)

                if "products" in data:
                    self.load_products(data["products"])
                if "terms" in data:
                    self.load_terms(data["terms"])

            self.session.commit()
            logger.info("Carga de datos completada.")

        except json.JSONDecodeError as e:
            self.session.rollback()
            logger.error(f"Error al decodificar JSON: {e}")
        except OSError as e:
            self.session.rollback()
            logger.error(f"Error al abrir/leer archivo: {e}")
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error inesperado: {e}")
        finally:
            self.session.close()

    def load_products(self, products):
        """Carga los productos en la base de datos."""
        for sku, product_data in products.items():
            try:
                pricing_data = PricingData(
                    sku=sku,
                    product_family=product_data.get("productFamily"),
                    database_engine=product_data.get("attributes", {}).get("databaseEngine"),
                    instance_type=product_data.get("attributes", {}).get("instanceType"),
                    memory=product_data.get("attributes", {}).get("memory"),
                    vcpu=product_data.get("attributes", {}).get("vcpu"),
                )
                self.session.add(pricing_data)
                self.session.flush() # Para obtener el ID generado

            except Exception as e:
                logger.error(f"Error al cargar producto {sku}: {e}")
                self.session.rollback()

    def load_terms(self, terms):
        """Carga los términos en la base de datos."""
        for term_type, term_data in terms.items():  # Itera sobre "OnDemand", "Reserved", etc.
            for sku, offer_term_data in term_data.items():  # Itera sobre SKUs
                for offer_term_code, term_info in offer_term_data.items():  # Itera sobre offerTermCodes
                    try:
                        term = Term(
                            sku=sku,
                            offerTermCode=term_info.get("offerTermCode"), # Usamos term_info aqui
                            effectiveDate=term_info.get("effectiveDate"), # Y aqui
                            termType=term_type,  # Usamos el tipo de término (OnDemand, Reserved)
                            leaseContractLength=term_info.get("termAttributes", {}).get("LeaseContractLength"),
                            purchaseOption=term_info.get("termAttributes", {}).get("PurchaseOption"),
                        )
                        self.session.add(term)
                        self.session.flush()  # Para obtener el ID generado

                        for rate_code, price_dim in term_info.get("priceDimensions", {}).items(): # Y aqui
                            price_dimension = PriceDimension(
                                term_id=term.id,
                                rateCode=rate_code,
                                unit=price_dim.get("unit"),
                                beginRange=price_dim.get("beginRange"),
                                endRange=price_dim.get("endRange"),
                                description=price_dim.get("description"),
                                priceUSD=price_dim.get("pricePerUnit", {}).get("USD"),
                            )
                            self.session.add(price_dimension)

                    except Exception as e:
                        logger.error(f"Error al cargar terminos para {sku} y {offer_term_code}: {e}")
                        self.session.rollback()

if __name__ == "__main__":
    loader = RdsPricingDataLoader(SQL_FILES, DATA)
    loader.process_json_files()