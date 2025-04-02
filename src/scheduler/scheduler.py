#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Configurar el path del proyecto para asegurar imports correctos
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.fetcher import FetcherData
from src.loader import LoaderData
from src.settings import PRICING_URL, DATA
from src.logger import setup_logger

# Configurar logger
logger = setup_logger("scheduler")

def run():
    try:
        
        pricing_fetcher = FetcherData(PRICING_URL, DATA)
        pricing_fetcher.fetching_data()

        rds_loader = LoaderData(DATA)
        rds_loader.loading_into_database()

        return True

    except Exception as e:
        logger.error(f"Error en la carga diaria: {str(e)}", exc_info=True)
        return False

if __name__ == "__main__":
    logger.info("Iniciando tarea programada de carga de datos")
    success = run()
    logger.info("Finalización de tarea programada de carga de datos")
    sys.exit(0 if success else 1)