# Logging helper
# 
# - Sets up logging config

import logging
from logging.handlers import RotatingFileHandler

def setup_logging(filename):

    # Logging config

    # Create logger
    logger = logging.getLogger("logs")
    logger.setLevel(level=logging.DEBUG)

    # Set formatter
    logFileFormatter = logging.Formatter(
        fmt=f"%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Set the handler
    fileHandler = logging.handlers.RotatingFileHandler(
    filename=filename, 
    maxBytes=5_000_000, 
    backupCount=3
    )

    # Set the logger

    fileHandler.setFormatter(logFileFormatter)
    fileHandler.setLevel(level=logging.DEBUG)
    logger.addHandler(fileHandler)

    return logger