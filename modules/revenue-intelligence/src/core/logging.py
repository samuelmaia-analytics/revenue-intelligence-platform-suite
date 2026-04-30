from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from pathlib import Path


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp_utc": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        for key in ("stage", "rows", "artifact", "provider", "status"):
            value = getattr(record, key, None)
            if value is not None:
                payload[key] = value
        return json.dumps(payload, ensure_ascii=True)


def configure_logging(level: str = "INFO", logs_dir: Path | None = None) -> None:
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    formatter = JsonFormatter()
    if not any(isinstance(handler, logging.StreamHandler) for handler in root_logger.handlers):
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        root_logger.addHandler(stream_handler)
    else:
        for handler in root_logger.handlers:
            handler.setFormatter(formatter)

    if logs_dir is not None:
        logs_dir.mkdir(parents=True, exist_ok=True)
        file_path = logs_dir / "pipeline.log"
        if not any(
            isinstance(handler, logging.FileHandler)
            and Path(handler.baseFilename) == file_path
            for handler in root_logger.handlers
        ):
            file_handler = logging.FileHandler(file_path, encoding="utf-8")
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
