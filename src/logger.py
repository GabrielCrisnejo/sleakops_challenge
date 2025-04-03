import os
import logging
from pathlib import Path

def setup_logger(name, testing=False):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    # File handler (only if not testing)
    if not testing:
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / 'logger.log'
        
        try:
            fh = logging.FileHandler(log_file, mode='a')
            fh.setFormatter(formatter)
            logger.addHandler(fh)
        except PermissionError:
            logger.warning("Could not create log file, using console only")
    
    return logger