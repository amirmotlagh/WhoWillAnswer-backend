import logging
from logging.handlers import RotatingFileHandler
import os
logging.basicConfig(level=logging.INFO)

LOG_DIR = "utils/logs"
LOG_FILE = "app.log"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)

log_format = "%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
log_level = logging.INFO
#Show in Consol
console_handler = logging.StreamHandler()
console_handler.setLevel(log_level)
console_handler.setFormatter(logging.Formatter(log_format))
#Save in file
file_handler = RotatingFileHandler(LOG_PATH, backupCount=2, encoding="utf-8")
file_handler.setLevel(log_level)
file_handler.setFormatter(logging.Formatter(log_format))

logger = logging.getLogger("AppLogger")
logger.setLevel(log_level)
logger.addHandler(console_handler)
logger.addHandler(file_handler)
def log_message(msg):
    logging.info(f"Message: {msg}")

# if __name__ == "__main__":
#     log_message("Hello from logger.py!")
#     logger.info("✅ Logger system initialized successfully.")
#     logger.debug("This is a debug message (won’t show unless log_level=DEBUG).")
#     logger.warning("⚠️ This is a warning message.")
#     logger.error("❌ This is an error message.")