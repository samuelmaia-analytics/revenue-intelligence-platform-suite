from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from platform_observability import write_monitoring_outputs


def test_write_monitoring_outputs_creates_expected_artifacts(tmp_path: Path) -> None:
    monthly = pd.DataFrame(
        [
            {"month": "2025-10", "SALES": 100_000.0},
            {"month": "2025-11", "SALES": 102_000.0},
            {"month": "2025-12", "SALES": 104_000.0},
            {"month": "2026-01", "SALES": 126_000.0},
        ]
    )

    pd.DataFrame(
        [
            {"action_id": "A1", "timestamp": "2026-03-05T00:00:00Z", "outcome": "accepted"},
            {"action_id": "A2", "timestamp": "2026-03-05T00:01:00Z", "outcome": "rejected"},
        ]
    ).to_csv(tmp_path / "action_adoption_log.csv", index=False)

    output = write_monitoring_outputs(tmp_path, monthly)

    assert (tmp_path / "drift_report.json").exists()
    assert (tmp_path / "action_adoption_metrics.json").exists()
    assert (tmp_path / "monitoring_summary.json").exists()
    assert output["action_adoption"]["total_events"] == 2
    assert output["drift"]["status"] in {"ok", "insufficient_history"}

    with (tmp_path / "monitoring_summary.json").open("r", encoding="utf-8") as fp:
        summary = json.load(fp)
    assert "drift" in summary
    assert "action_adoption" in summary
