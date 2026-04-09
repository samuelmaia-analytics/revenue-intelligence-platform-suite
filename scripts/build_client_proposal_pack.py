from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHOWCASE_DIR = ROOT / "reports" / "showcase"
OUTPUT_DIR = ROOT / "dist" / "client-proposal-pack"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "packages") not in sys.path:
    sys.path.insert(0, str(ROOT / "packages"))

from common.configuration import load_solution_configuration  # noqa: E402
from scripts.build_synthetic_benchmark import main as build_synthetic_benchmark  # noqa: E402


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    build_synthetic_benchmark()

    solution_profile = _load_json(SHOWCASE_DIR / "solution_profile.json")
    scorecard = _load_json(SHOWCASE_DIR / "data_quality_scorecard.json")
    insights = _load_json(SHOWCASE_DIR / "executive_insights.json")
    summary = _load_json(SHOWCASE_DIR / "summary.json")
    benchmark_path = ROOT / "dist" / "benchmarks" / "industry_benchmark.json"
    benchmark = json.loads(benchmark_path.read_text(encoding="utf-8")) if benchmark_path.exists() else []
    config = load_solution_configuration(
        client_profile=solution_profile.get("profile_id", "saas_b2b"),
        deployment_env=solution_profile.get("deployment_env", "showcase"),
        solution_package=solution_profile.get("package", {}).get("package_id", "revenue_command_center"),
    )

    industry = solution_profile.get("industry", "General")
    relevant_benchmark = next(
        (row for row in benchmark if row.get("industry", "").lower() == industry.lower()),
        None,
    )
    brand = solution_profile.get("brand", {})
    narrative = solution_profile.get("narrative", {})
    commercial_defaults = config.get("commercial_defaults", {})
    scope_options = config.get("scope_options", {})
    proposal_client_name = os.getenv("PROPOSAL_CLIENT_NAME", solution_profile.get("client_name", "Client"))
    proposal_setup_fee = os.getenv(
        "PROPOSAL_SETUP_FEE", commercial_defaults.get("setup_fee_range", "$25k-$60k")
    )
    proposal_monthly_fee = os.getenv(
        "PROPOSAL_MONTHLY_FEE", commercial_defaults.get("monthly_service_range", "$6k-$18k")
    )
    proposal_timeline = os.getenv(
        "PROPOSAL_TIMELINE", commercial_defaults.get("implementation_timeline", "4-8 weeks")
    )

    md_path = OUTPUT_DIR / "client_proposal.md"
    md_lines = [
        "# Client Proposal Pack",
        "",
        f"Client: {proposal_client_name}",
        f"Industry: {industry}",
        f"Buyer: {solution_profile.get('executive_buyer', 'n/a')}",
        f"Package: {solution_profile.get('package', {}).get('name', 'n/a')}",
        "",
        "## Executive Positioning",
        f"- {narrative.get('headline', '')}",
        f"- {narrative.get('value_proposition', '')}",
        "",
        "## Business Case",
        f"- Current value at risk: ${summary.get('total_value_at_risk_usd', 0.0):,.0f}",
        f"- Current quality score: {scorecard.get('overall_score', 0.0):.1f}",
        f"- Current NRR: {summary.get('nrr_latest', 0.0):.1%}",
        "",
        "## Why Now",
    ]
    for insight in insights.get("insights", []):
        md_lines.append(f"- {insight['headline']} {insight['detail']}")
    md_lines.extend(["", "## Recommended Delivery Model"])
    md_lines.append(f"- {solution_profile.get('package', {}).get('delivery_model', 'n/a')}")
    md_lines.extend(["", "## Scope Recommendation"])
    for scope_name, items in scope_options.items():
        md_lines.append(f"- {scope_name.title()}: {', '.join(items)}")
    md_lines.extend(["", "## Commercial Structure"])
    md_lines.append(f"- Setup fee: {proposal_setup_fee}")
    md_lines.append(f"- Monthly recurring service: {proposal_monthly_fee}")
    md_lines.append(f"- Estimated implementation timeline: {proposal_timeline}")
    md_lines.extend(["", "## Benchmark Reference"])
    if relevant_benchmark:
        md_lines.append(
            f"- {relevant_benchmark['industry']} target NRR: {relevant_benchmark['nrr_target']:.0%}; "
            f"churn ceiling: {relevant_benchmark['gross_churn_ceiling']:.0%}; "
            f"quality target: {relevant_benchmark['quality_score_target']}"
        )
    md_lines.extend(
        [
            "",
            "## Copyright And Usage",
            "Copyright (c) 2026 Samuel Maia. This proposal pack and its associated assets are proprietary.",
            "Public review or client sharing for evaluation does not grant reuse, redistribution, sublicensing, or derivative rights.",
        ]
    )
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    html_path = OUTPUT_DIR / "client_proposal.html"
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Client Proposal Pack</title>
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; background: linear-gradient(180deg, {brand.get('hero_gradient_start', '#eef6ff')} 0%, {brand.get('hero_gradient_end', '#ffffff')} 100%); color: {brand.get('secondary_color', '#122033')}; }}
    .wrap {{ max-width: 1080px; margin: 0 auto; padding: 40px 24px 60px; }}
    .hero, .panel {{ background: #fff; border-radius: 24px; padding: 28px; box-shadow: 0 10px 24px rgba(15, 23, 42, 0.08); }}
    .hero h1 {{ margin: 0 0 8px; font-size: 40px; }}
    .pill {{ display: inline-block; padding: 6px 10px; border-radius: 999px; background: {brand.get('accent_soft', '#dff7f4')}; color: {brand.get('primary_color', '#0f766e')}; font-size: 12px; font-weight: 700; }}
    .grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 22px; }}
    .card {{ background: #fff; border-radius: 20px; padding: 20px; box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06); }}
    .label {{ font-size: 12px; color: #5b6b81; text-transform: uppercase; }}
    .value {{ margin-top: 8px; font-size: 28px; font-weight: 700; }}
    .panel {{ margin-top: 24px; }}
    ul {{ margin: 0; padding-left: 18px; }}
    li {{ margin-bottom: 10px; }}
    .notice {{ margin-top: 24px; padding: 16px 18px; border-radius: 18px; background: #fff7ed; color: #9a3412; border: 1px solid #fed7aa; font-size: 14px; }}
    .footer {{ margin-top: 28px; color: #5b6b81; font-size: 13px; text-align: center; }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="hero">
      <span class="pill">{solution_profile.get('package', {}).get('name', 'Proposal')}</span>
      <h1>{proposal_client_name} Proposal Pack</h1>
      <p><strong>{narrative.get('headline', '')}</strong><br>{narrative.get('value_proposition', '')}</p>
    </div>
    <div class="grid">
      <div class="card"><div class="label">Value At Risk</div><div class="value">${summary.get('total_value_at_risk_usd', 0.0):,.0f}</div></div>
      <div class="card"><div class="label">NRR</div><div class="value">{summary.get('nrr_latest', 0.0):.1%}</div></div>
      <div class="card"><div class="label">Quality Score</div><div class="value">{scorecard.get('overall_score', 0.0):.1f}</div></div>
    </div>
    <div class="panel">
      <h2>Why This Matters</h2>
      <ul>{''.join(f"<li>{insight['headline']} {insight['detail']}</li>" for insight in insights.get('insights', []))}</ul>
    </div>
    <div class="panel">
      <h2>Delivery Model</h2>
      <p>{solution_profile.get('package', {}).get('delivery_model', 'n/a')}</p>
      <p>Executive buyer: {solution_profile.get('executive_buyer', 'n/a')}</p>
    </div>
    <div class="panel">
      <h2>Commercial Structure</h2>
      <p>Setup fee: <strong>{proposal_setup_fee}</strong></p>
      <p>Monthly recurring service: <strong>{proposal_monthly_fee}</strong></p>
      <p>Estimated implementation timeline: <strong>{proposal_timeline}</strong></p>
    </div>
    <div class="notice">
      Copyright (c) 2026 Samuel Maia. This proposal pack is proprietary and shared for commercial evaluation only.
      Public visibility does not grant reuse, redistribution, sublicensing, or derivative rights.
    </div>
    <div class="footer">Proprietary commercial asset | Samuel Maia</div>
  </div>
</body>
</html>"""
    html_path.write_text(html, encoding="utf-8")

    json_path = OUTPUT_DIR / "client_proposal.json"
    json_path.write_text(
        json.dumps(
            {
                "solution_profile": solution_profile,
                "summary": summary,
                "scorecard": scorecard,
                "benchmark": relevant_benchmark,
                "insights": insights,
                "proposal_client_name": proposal_client_name,
                "commercial_structure": {
                    "setup_fee": proposal_setup_fee,
                    "monthly_service": proposal_monthly_fee,
                    "timeline": proposal_timeline,
                },
                "scope_options": scope_options,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Client proposal pack generated in {OUTPUT_DIR}")


if __name__ == "__main__":
    os.environ.setdefault("CLIENT_PROFILE", "saas_b2b")
    main()
