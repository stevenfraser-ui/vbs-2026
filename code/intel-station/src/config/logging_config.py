"""Centralized logging configuration for Intel Station."""

import logging
import logging.config
from pathlib import Path


def setup_logging(log_dir: Path | None = None, log_level: str = "INFO") -> None:
    """Configure logging for the application.

    Sets up two handlers:
    - Console (StreamHandler): log_level, concise format
    - Rotating file (RotatingFileHandler): DEBUG, verbose format

    Third-party libraries are suppressed to WARNING to reduce noise.

    Args:
        log_dir: Directory for the rotating log file. Defaults to data/logs/
                 relative to the project root. Created if it doesn't exist.
        log_level: Minimum level for the console handler (e.g. "INFO", "DEBUG").
                   Overridden by the LOG_LEVEL env var in settings.py.
    """
    if log_dir is None:
        # data/ lives two levels above this config/ directory
        log_dir = Path(__file__).resolve().parent.parent.parent / "data" / "logs"

    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = str(log_dir / "intel_station.log")

    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                "datefmt": "%H:%M:%S",
            },
            "file": {
                "format": (
                    "%(asctime)s [%(levelname)s] %(name)s "
                    "(%(funcName)s:%(lineno)d): %(message)s"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "console",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "file",
                "filename": log_file,
                "maxBytes": 5 * 1024 * 1024,  # 5 MB
                "backupCount": 3,
                "encoding": "utf-8",
            },
        },
        "loggers": {
            # App loggers — inherit root level
            "src": {
                "handlers": ["console", "file"],
                "level": "DEBUG",
                "propagate": False,
            },
            # Suppress noisy third-party libraries
            "streamlit": {"level": "WARNING", "propagate": True},
            "strands": {"level": "WARNING", "propagate": True},
            "urllib3": {"level": "WARNING", "propagate": True},
            "httpx": {"level": "WARNING", "propagate": True},
            "httpcore": {"level": "WARNING", "propagate": True},
            "ollama": {"level": "WARNING", "propagate": True},
            "watchdog": {"level": "WARNING", "propagate": True},
        },
        "root": {
            "level": "WARNING",
            "handlers": ["console", "file"],
        },
    }

    logging.config.dictConfig(config)
