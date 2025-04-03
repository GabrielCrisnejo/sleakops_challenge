import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.settings import DB_URL, DATA
from src.models import Base, PricingData, Term, PriceDimension
from src.logger import setup_logger

# Logger configuration
logger = setup_logger("loader")

class LoaderData:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.engine = create_engine(DB_URL)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def loading_into_database(self):
        """Processes JSON files and loads data into the database."""
        try:
            json_files = [f for f in os.listdir(self.data_dir) if f.endswith(".json")]

            for file_name in json_files:
                file_path = os.path.join(self.data_dir, file_name)
                logger.info(f"Processing file: {file_name}")

                with open(file_path, "r") as f:
                    data = json.load(f)

                if "products" in data:
                    self.load_products(data["products"])
                if "terms" in data:
                    self.load_terms(data["terms"])

            self.session.commit()
            logger.info("Data loading completed.")

        except json.JSONDecodeError as e:
            self.session.rollback()
            logger.error(f"JSON decoding error: {e}")
        except OSError as e:
            self.session.rollback()
            logger.error(f"File open/read error: {e}")
        except Exception as e:
            self.session.rollback()
            logger.error(f"Unexpected error: {e}")
        finally:
            self.session.close()

    def load_products(self, products):
        """Loads products into the database."""
        for sku, product_data in products.items():
            try:
                # Check if the sku already exists
                existing_product = self.session.query(PricingData).filter(PricingData.sku == sku).first()

                if existing_product:
                    logger.info(f"SKU {sku} already exists. Skipping insert.")
                    continue

                # Insert the product if it doesn't exist
                pricing_data = PricingData(
                    sku=sku,
                    product_family=product_data.get("productFamily"),
                    database_engine=product_data.get("attributes", {}).get("databaseEngine"),
                    instance_type=product_data.get("attributes", {}).get("instanceType"),
                    memory=product_data.get("attributes", {}).get("memory"),
                    vcpu=product_data.get("attributes", {}).get("vcpu"),
                )
                self.session.add(pricing_data)
                self.session.flush()  # To get the generated ID

            except Exception as e:
                logger.error(f"Error loading product {sku}: {e}")
                self.session.rollback()

    def load_terms(self, terms):
        """Loads terms into the database."""
        for term_type, term_data in terms.items():  # Iterates over "OnDemand", "Reserved", etc.
            for sku, offer_term_data in term_data.items():  # Iterates over SKUs
                for offer_term_code, term_info in offer_term_data.items():  # Iterates over offerTermCodes
                    try:
                        term = Term(
                            sku=sku,
                            offerTermCode=term_info.get("offerTermCode"),  # Using term_info here
                            effectiveDate=term_info.get("effectiveDate"),  # And here
                            termType=term_type,  # Using term type (OnDemand, Reserved)
                            leaseContractLength=term_info.get("termAttributes", {}).get("LeaseContractLength"),
                            purchaseOption=term_info.get("termAttributes", {}).get("PurchaseOption"),
                        )
                        self.session.add(term)
                        self.session.flush()  # To get the generated ID

                        for rate_code, price_dim in term_info.get("priceDimensions", {}).items():  # And here
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
                        logger.error(f"Error loading terms for {sku} and {offer_term_code}: {e}")
                        self.session.rollback()
