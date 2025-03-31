import uvicorn
from src.routes import router as pricing_router
from src.pricing_loader import PricingDataLoader
from src.loader import RdsPricingDataLoader
from src.config import PRICING_URL, DATA, SQL_FILES
from src.logger import setup_logger
from fastapi import FastAPI

# Logger configuration
logger = setup_logger("fetch_pricings")

app = FastAPI()  # Mueve la definición de app fuera del bloque if __name__
app.include_router(pricing_router)

def run_data_loaders():
    """Instancia y ejecuta PricingDataLoader y RdsPricingDataLoader."""
    try:
        logger.info("Ejecutando PricingDataLoader...")
        pricing_loader = PricingDataLoader(PRICING_URL, DATA)
        pricing_loader.load_pricing_data()
        logger.info("PricingDataLoader ejecutado con éxito.")

        logger.info("Ejecutando RdsPricingDataLoader...")
        rds_loader = RdsPricingDataLoader(SQL_FILES, DATA)
        rds_loader.process_json_files()
        logger.info("RdsPricingDataLoader ejecutado con éxito.")
    except Exception as e:
        logger.error(f"Error al ejecutar los loaders: {e}")

if __name__ == "__main__":
    run_data_loaders()  # Ejecutar los loaders antes de iniciar la API
    uvicorn.run(app, host="127.0.0.1", port=8000)