import datetime
import json
from typing import Any, Dict, Optional

class Logger:
    _instance = None
    _log_file = "logs.txt"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def _log(self, log_type: str, message: str, metadata: Optional[Dict[str, Any]] = None):
        log_entry = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "type": log_type,
            "message": message,
            "metadata": metadata or {}
        }
        with open(self._log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")

    def info(self, message: str, metadata: Optional[Dict[str, Any]] = None):
        self._log("INFO", message, metadata)

    def warning(self, message: str, metadata: Optional[Dict[str, Any]] = None):
        self._log("WARNING", message, metadata)

    def error(self, message: str, metadata: Optional[Dict[str, Any]] = None):
        self._log("ERROR", message, metadata)

    def debug(self, message: str, metadata: Optional[Dict[str, Any]] = None):
        self._log("DEBUG", message, metadata)

    def event(self, message: str, metadata: Optional[Dict[str, Any]] = None):
        self._log("EVENT", message, metadata)

    def data(self, message: str, metadata: Optional[Dict[str, Any]] = None):
        self._log("DATA", message, metadata)

# Usage example:
# logger = Logger()
# logger.info("Application started", {"user": "alice"})
