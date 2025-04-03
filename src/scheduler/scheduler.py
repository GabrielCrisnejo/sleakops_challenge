#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Configure project path to ensure correct imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.fetcher import FetcherData
from src.loader import LoaderData
from src.settings import PRICING_URL, DATA
from src.logger import setup_logger

# Configure logger
logger = setup_logger("scheduler")

def run():
    """Execute the daily data loading pipeline."""
    try:
        logger.debug("Starting data fetching process")
        pricing_fetcher = FetcherData(PRICING_URL, DATA)
        pricing_fetcher.fetching_data()

        logger.debug("Starting database loading process")
        rds_loader = LoaderData(DATA)
        rds_loader.loading_into_database()

        return True

    except Exception as e:
        logger.error(f"Error in daily data load: {str(e)}", exc_info=True)
        return False

if __name__ == "__main__":
    logger.info("Starting scheduled data loading task")
    success = run()
    status = "completed successfully" if success else "failed"
    logger.info(f"Scheduled data loading task {status}")
    sys.exit(0 if success else 1)