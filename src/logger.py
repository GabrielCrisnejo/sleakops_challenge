import logging
import os
from src.settings import LOG_FILE

def setup_logger(name: str, log_file: str = LOG_FILE, level: int = logging.INFO, to_file: bool = True) -> logging.Logger:
    """Set up and return a logger with optional file logging."""
    logger = logging.getLogger(name)

    if logger.hasHandlers():
        return logger

    logger.setLevel(level)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if to_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file, mode='a')  # Cambiado a modo 'a' (append)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger