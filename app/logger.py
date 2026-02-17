import logging.config
import os
from pathlib import Path
import copy

LOG_DIR = Path(__file__).parent / "logs"

LOGGING_CONFIG = {
    "version": 1,

    "disable_existing_loggers": False,

    # ---------- FORMATTERS ----------
    "formatters": {
        "default": {
            "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        },
        "access": {
            "format": "%(asctime)s | ACCESS | %(client_addr)s | %(request_line)s | %(status_code)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "detailed": {
            "format": "%(asctime)s | %(levelname)s | %(name)s | "
                      "%(filename)s:%(lineno)d | %(message)s",
        },
    },

    # ---------- HANDLERS ----------
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": str(LOG_DIR / "app.log"),
            "maxBytes": 5 * 1024 * 1024,  # 5MB
            "backupCount": 5,
            "encoding": "utf-8",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },

    # ---------- LOGGERS ----------
    "loggers": {

        "app": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },


        "fastapi": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },


        "uvicorn.access": {
            "handlers": ["access"],
            "level": "INFO",
            "propagate": False,
        },


        "uvicorn.error": {
            "handlers": ["console", "file"],
            "level": "WARNING",
            "propagate": False,
        },
    },

    # ---------- ROOT ----------
    "root": {
        "level": "WARNING",
        "handlers": ["console", "file"],
    },
}

def get_log_level() -> str:
    return os.getenv("LOG_LEVEL", "INFO").upper()

def get_log_file_path() -> str:
    return os.getenv("LOG_FILE_PATH", str(LOG_DIR / "app.log"))

def get_backup_count() -> int:
    return int(os.getenv("LOG_BACKUP_COUNT", "5"))

def get_max_bytes() -> int:
    return int(os.getenv("LOG_MAX_BYTES", str(5 * 1024 * 1024)))

def setup_logging() -> None:
    LOG_DIR.mkdir(exist_ok=True)
    config = copy.deepcopy(LOGGING_CONFIG)
    config["handlers"]["console"]["level"] = get_log_level()
    config["handlers"]["file"]["filename"] = get_log_file_path()
    config["handlers"]["file"]["maxBytes"] = get_max_bytes()
    config["handlers"]["file"]["backupCount"] = get_backup_count()

    logging.config.dictConfig(config)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

# for test
if __name__ == "__main__":
    import logging.config

    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger("app")

    logger.debug("DEBUG test")
    logger.info("INFO test")
    logger.warning("WARNING test")
    logger.error("ERROR test")