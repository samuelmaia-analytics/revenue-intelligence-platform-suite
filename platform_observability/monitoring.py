from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


def _to_revenue_frame(monthly_revenue: pd.DataFrame) -> pd.DataFrame:
    if "revenue_usd" in monthly_revenue.columns:
        revenue = monthly_revenue[["month", "revenue_usd"]].copy()
    else:
        revenue = monthly_revenue[["month", "SALES"]].rename(columns={"SALES": "revenue_usd"}).copy()
    revenue["revenue_usd"] = pd.to_numeric(revenue["revenue_usd"], errors="coerce").fillna(0.0)
    return revenue.sort_values("month").reset_index(drop=True)


def build_drift_report(monthly_revenue: pd.DataFrame) -> dict[str, Any]:
    revenue = _to_revenue_frame(monthly_revenue)
    if len(revenue) < 4:
        return {
            "status": "insufficient_history",
            "drift_detected": False,
            "drift_score": 0.0,
            "baseline_mean_revenue_usd": 0.0,
            "recent_mean_revenue_usd": float(revenue["revenue_usd"].mean() if not revenue.empty else 0.0),
            "baseline_window_months": 0,
            "recent_window_months": len(revenue),
            "generated_at": pd.Timestamp.utcnow().isoformat(),
        }

    window = min(3, max(1, len(revenue) // 2))
    baseline = revenue.iloc[:-window]
    recent = revenue.iloc[-window:]
    baseline_mean = float(baseline["revenue_usd"].mean()) if not baseline.empty else 0.0
    recent_mean = float(recent["revenue_usd"].mean()) if not recent.empty else 0.0
    drift_score = abs(recent_mean - baseline_mean) / max(abs(baseline_mean), 1.0)

    return {
        "status": "ok",
        "drift_detected": drift_score > 0.2,
        "drift_score": round(float(drift_score), 4),
        "baseline_mean_revenue_usd": round(baseline_mean, 2),
        "recent_mean_revenue_usd": round(recent_mean, 2),
        "baseline_window_months": len(baseline),
        "recent_window_months": len(recent),
        "generated_at": pd.Timestamp.utcnow().isoformat(),
    }


def build_action_adoption_metrics(action_log_csv_path: Path) -> dict[str, Any]:
    if not action_log_csv_path.exists():
        return {
            "status": "no_events",
            "total_events": 0,
            "accepted_events": 0,
            "in_progress_events": 0,
            "rejected_events": 0,
            "adoption_rate": 0.0,
            "generated_at": pd.Timestamp.utcnow().isoformat(),
        }

    events = pd.read_csv(action_log_csv_path)
    if events.empty or "outcome" not in events.columns:
        return {
            "status": "no_events",
            "total_events": 0,
            "accepted_events": 0,
            "in_progress_events": 0,
            "rejected_events": 0,
            "adoption_rate": 0.0,
            "generated_at": pd.Timestamp.utcnow().isoformat(),
        }

    counts = events["outcome"].value_counts()
    total = int(len(events))
    accepted = int(counts.get("accepted", 0))
    in_progress = int(counts.get("in_progress", 0))
    rejected = int(counts.get("rejected", 0))
    adoption_rate = accepted / total if total else 0.0

    return {
        "status": "ok",
        "total_events": total,
        "accepted_events": accepted,
        "in_progress_events": in_progress,
        "rejected_events": rejected,
        "adoption_rate": round(float(adoption_rate), 4),
        "generated_at": pd.Timestamp.utcnow().isoformat(),
    }


def write_monitoring_outputs(output_dir: Path, monthly_revenue: pd.DataFrame) -> dict[str, dict[str, Any]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    drift = build_drift_report(monthly_revenue)
    adoption = build_action_adoption_metrics(output_dir / "action_adoption_log.csv")

    drift_path = output_dir / "drift_report.json"
    adoption_path = output_dir / "action_adoption_metrics.json"
    summary_path = output_dir / "monitoring_summary.json"

    with drift_path.open("w", encoding="utf-8") as fp:
        json.dump(drift, fp, indent=2)
    with adoption_path.open("w", encoding="utf-8") as fp:
        json.dump(adoption, fp, indent=2)
    with summary_path.open("w", encoding="utf-8") as fp:
        json.dump({"drift": drift, "action_adoption": adoption}, fp, indent=2)

    return {"drift": drift, "action_adoption": adoption}
