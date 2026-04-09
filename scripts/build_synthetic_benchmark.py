from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "dist" / "benchmarks"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    benchmark = pd.DataFrame(
        [
            {
                "profile": "saas_b2b",
                "industry": "SaaS",
                "package": "Revenue Command Center",
                "nrr_target": 0.90,
                "gross_churn_ceiling": 0.10,
                "value_at_risk_band_usd": "100k-300k",
                "quality_score_target": 85,
            },
            {
                "profile": "healthtech_growth",
                "industry": "Healthtech",
                "package": "Retention Intelligence",
                "nrr_target": 0.88,
                "gross_churn_ceiling": 0.08,
                "value_at_risk_band_usd": "80k-220k",
                "quality_score_target": 85,
            },
            {
                "profile": "retail_omnichannel",
                "industry": "Retail",
                "package": "Commercial Performance Analytics",
                "nrr_target": 0.85,
                "gross_churn_ceiling": 0.12,
                "value_at_risk_band_usd": "120k-350k",
                "quality_score_target": 82,
            },
        ]
    )
    csv_path = OUTPUT_DIR / "industry_benchmark.csv"
    benchmark.to_csv(csv_path, index=False)

    json_path = OUTPUT_DIR / "industry_benchmark.json"
    json_path.write_text(json.dumps(benchmark.to_dict(orient="records"), indent=2), encoding="utf-8")
    print(f"Synthetic benchmark generated: {csv_path}")


if __name__ == "__main__":
    main()
