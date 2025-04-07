

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)


logger = logging.getLogger("logistics_app")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    '[%(asctime)s] [%(levelname)s] %(name)s: %(message)s'
)


console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)


file_handler = RotatingFileHandler("logs/app.log", maxBytes=1_000_000, backupCount=5)
file_handler.setFormatter(formatter)


if not logger.hasHandlers():
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
