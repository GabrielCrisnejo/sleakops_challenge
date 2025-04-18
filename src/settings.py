import os
from pathlib import Path

# Define base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database configuration
DB_NAME = os.getenv("DB_NAME", "pricing_db")
DB_USER = os.getenv("DB_USER", "gcrisnejo")
DB_PASSWORD = os.getenv("DB_PASSWORD", "gcrisnejo")
#DB_HOST = os.getenv("DB_HOST", "localhost")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_URL = os.getenv("DB_URL", f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# URL to fetch RDS pricing data
PRICING_URL = "https://sleakops-interview-tests.s3.us-east-1.amazonaws.com/rds_us_east_1_pricing.json"

# Logging configuration
LOG_FILE = os.getenv("LOG_FILE", str(os.path.join(BASE_DIR, "logs", "logger.log")))
LOG_FILE_TEST = os.getenv("LOG_FILE", str(os.path.join(BASE_DIR, "logs", "logger_test.log")))
DATA = os.getenv("DATA", str(BASE_DIR / "data"))

# Flag to indicate if we're in a testing environment
TESTING = os.getenv("TESTING", False)  # Get environment variable or False if not defined