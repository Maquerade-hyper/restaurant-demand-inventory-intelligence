import logging
import platform
import sys

from .config import get_settings
from .db import check_database_connection

logger = logging.getLogger(__name__)


def run_health_check() -> dict:
    settings = get_settings()
    result = {
        "application": settings.app_name,
        "environment": settings.app_env,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "database": {"status": "unknown"},
    }

    try:
        result["database"] = check_database_connection()
    except Exception as exc:  # health check must report failure without leaking secrets
        logger.exception("database_health_check_failed")
        result["database"] = {
            "status": "error",
            "error_type": type(exc).__name__,
        }

    result["status"] = "ok" if result["database"]["status"] == "ok" else "degraded"
    return result
