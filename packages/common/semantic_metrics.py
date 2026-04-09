from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _catalog_path() -> Path:
    return Path(__file__).resolve().parents[2] / "config" / "semantic_metrics.json"


def load_semantic_metric_catalog() -> dict[str, Any]:
    with _catalog_path().open("r", encoding="utf-8") as fp:
        return json.load(fp)


def list_semantic_metrics() -> list[dict[str, Any]]:
    catalog = load_semantic_metric_catalog()
    return catalog.get("metrics", [])


def get_semantic_metric(metric_id: str) -> dict[str, Any]:
    metrics = {metric["metric_id"]: metric for metric in list_semantic_metrics()}
    if metric_id not in metrics:
        raise KeyError(metric_id)
    return metrics[metric_id]
