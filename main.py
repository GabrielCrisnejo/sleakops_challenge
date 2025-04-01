import uvicorn
from src.routes import router as pricing_router
from src.fetcher import FetcherData
from src.loader import LoaderData
from src.settings import PRICING_URL, DATA
from src.logger import setup_logger
from fastapi import FastAPI
import logging


import time
from alembic import command
from alembic.config import Config
from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine
import os
import threading

# Logger configuration
logger = setup_logger("fetch_pricings")

app = FastAPI()
app.include_router(pricing_router)

# Configuración de la base de datos
DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def run_migrations():
    """Ejecuta las migraciones de Alembic."""
    # Función de reintento para la conexión a la base de datos
    def wait_for_db():
        retries = 5
        while retries > 0:
            try:
                engine.connect()
                print("Database is ready!")
                return True
            except OperationalError:
                print("Database not ready, retrying...")
                time.sleep(2)
                retries -= 1
        return False

    # Ejecutar migraciones de Alembic
    if wait_for_db():
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
    else:
        print("Failed to connect to the database. Exiting.")
        exit(1)

# # Logger configuration
# logger = setup_logger("fetch_pricings")

# app = FastAPI()

def run():
    """Instancia y ejecuta FetcherData y LoaderData."""
    try:
        logger.info("Ejecutando FetcherData...")
        pricing_loader = FetcherData(PRICING_URL, DATA)
        logger.debug(f"FetcherData initialized with URL: {PRICING_URL}, DATA: {DATA}")
        pricing_loader.load_pricing_data()
        logger.info("FetcherData ejecutado con éxito.")

        logger.info("Ejecutando LoaderData...")
        rds_loader = LoaderData(DATA)
        logger.debug(f"LoaderData initialized with DATA: {DATA}")
        rds_loader.process_json_files()
        logger.info("LoaderData ejecutado con éxito.")

        for handler in logging.getLogger().handlers:
            if isinstance(handler, logging.FileHandler):
                handler.flush()
                break

    except Exception as e:
        logger.error(f"Error al ejecutar los loaders: {e}")

if __name__ == "__main__":
    run_migrations()
    run()
    logging.shutdown()
    # uvicorn.run(app, host="127.0.0.1", port=8000)
    uvicorn.run(app, host="0.0.0.0", port=8000) # Cambiado a 0.0.0.0

    #threading.Thread(target=run).start() # Ejecutar run() en un hilo separado
    #uvicorn.run(app, host="0.0.0.0", port=8000) # Iniciar uvicorn