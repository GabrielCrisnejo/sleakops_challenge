import uvicorn
from src.routes import router as pricing_router
from src.fetcher import FetcherData
from src.loader import LoaderData
from src.settings import PRICING_URL, DATA
from src.logger import setup_logger
from fastapi import FastAPI

# Logger configuration
logger = setup_logger("main")

app = FastAPI()
app.include_router(pricing_router)

def run():
    """Instancia y ejecuta FetcherData y LoaderData."""
    try:
        logger.info("Ejecutando FetcherData...")
        pricing_fetcher = FetcherData(PRICING_URL, DATA)
        logger.debug(f"FetcherData initialized with URL: {PRICING_URL}, DATA: {DATA}")
        pricing_fetcher.fetching_data()
        logger.info("FetcherData ejecutado con éxito.")

        logger.info("Ejecutando LoaderData...")
        rds_loader = LoaderData(DATA)
        logger.debug(f"LoaderData initialized with DATA: {DATA}")
        rds_loader.loading_into_database()
        logger.info("LoaderData ejecutado con éxito.")

    except Exception as e:
        logger.error(f"Error al ejecutar los loaders: {e}")

if __name__ == "__main__":
    run()
    uvicorn.run(app, host="0.0.0.0", port=8000)

    