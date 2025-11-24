# error_handler.py

import logging

LOG_FILE = "error.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def log_error(context: str, exc: Exception) -> None:
    """Log errors with some context information."""
    logging.error("%s: %s", context, str(exc))
