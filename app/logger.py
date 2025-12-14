import logging.config
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

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
            "filename": "logs/app.log",
            "maxBytes": 5 * 1024 * 1024,  # 5MB
            "backupCount": 5,
            "encoding": "utf-8",
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
            "handlers": ["console"],
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
# for test
if __name__ == "__main__":
    import logging.config

    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger("app")

    logger.debug("DEBUG test")
    logger.info("INFO test")
    logger.warning("WARNING test")
    logger.error("ERROR test")