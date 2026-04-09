from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "packages") not in sys.path:
    sys.path.insert(0, str(ROOT / "packages"))

from common.configuration import load_solution_configuration  # noqa: E402
from common.contracts import validate_contract  # noqa: E402
from common.semantic_metrics import list_semantic_metrics  # noqa: E402


SHOWCASE_DIR = ROOT / "reports" / "showcase"


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def main() -> None:
    solution_profile = _load_json(SHOWCASE_DIR / "solution_profile.json")
    summary = _load_json(SHOWCASE_DIR / "summary.json")
    scorecard = _load_json(SHOWCASE_DIR / "data_quality_scorecard.json")
    insights = _load_json(SHOWCASE_DIR / "executive_insights.json")
    adoption = _load_json(SHOWCASE_DIR / "action_adoption_metrics.json")

    config = load_solution_configuration(
        client_profile=solution_profile.get("profile_id", "saas_b2b"),
        deployment_env=solution_profile.get("deployment_env", "showcase"),
        solution_package=solution_profile.get("package", {}).get("package_id", "revenue_command_center"),
    )

    contract_errors = []
    contract_errors.extend(validate_contract(summary, "showcase_summary.v1.schema.json"))
    contract_errors.extend(validate_contract(insights, "executive_insight_report.v1.schema.json"))
    if contract_errors:
        raise SystemExit(f"Contract validation failed: {contract_errors}")

    metric_ids = {metric["metric_id"] for metric in list_semantic_metrics()}
    required_metrics = {
        "latest_revenue_usd",
        "nrr_latest",
        "gross_churn_latest",
        "total_value_at_risk_usd",
        "overall_score",
        "adoption_rate",
    }
    if not required_metrics.issubset(metric_ids):
        missing = sorted(required_metrics - metric_ids)
        raise SystemExit(f"Semantic metric catalog missing required metrics: {missing}")

    thresholds = config.get("thresholds", {})
    nrr_floor = thresholds.get("nrr_floor", 0.9)
    gross_churn_ceiling = thresholds.get("gross_churn_ceiling", 0.1)
    scorecard_target = config.get("governance", {}).get("scorecard_target", 85)
    freshness_sla_days = config.get("governance", {}).get("freshness_sla_days", 30)

    failures: list[str] = []
    if float(summary["nrr_latest"]) < nrr_floor:
        failures.append(f"NRR below floor: {summary['nrr_latest']} < {nrr_floor}")
    if float(summary["gross_churn_latest"]) > gross_churn_ceiling:
        failures.append(f"Gross churn above ceiling: {summary['gross_churn_latest']} > {gross_churn_ceiling}")
    if float(scorecard["overall_score"]) < max(scorecard_target - 5, 0):
        failures.append(
            f"Quality score below tolerated floor: {scorecard['overall_score']} < {max(scorecard_target - 5, 0)}"
        )
    if int(scorecard.get("dimensions", {}).get("freshness_days", 9999)) > freshness_sla_days + 7:
        failures.append(
            "Freshness exceeded tolerated window: "
            f"{scorecard.get('dimensions', {}).get('freshness_days')} > {freshness_sla_days + 7}"
        )
    if "adoption_rate" in adoption and float(adoption["adoption_rate"]) < 0:
        failures.append("Adoption rate cannot be negative.")

    if failures:
        raise SystemExit("Showcase validation failed: " + "; ".join(failures))

    print("Showcase artifacts validated successfully.")


if __name__ == "__main__":
    main()
