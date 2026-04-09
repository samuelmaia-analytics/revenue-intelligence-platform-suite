from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "packages") not in sys.path:
    sys.path.insert(0, str(ROOT / "packages"))


SHOWCASE_DIR = ROOT / "reports" / "showcase"
OUTPUT_DIR = ROOT / "dist" / "executive-review-pack"


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def build_pack() -> dict[str, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    summary = _load_json(SHOWCASE_DIR / "summary.json")
    scorecard = _load_json(SHOWCASE_DIR / "data_quality_scorecard.json")
    insights = _load_json(SHOWCASE_DIR / "executive_insights.json")
    solution_profile = _load_json(SHOWCASE_DIR / "solution_profile.json")
    adoption = _load_json(SHOWCASE_DIR / "action_adoption_metrics.json")
    top_actions = pd.read_csv(SHOWCASE_DIR / "top_actions.csv").head(10)
    brand = solution_profile.get("brand", {})
    narrative = solution_profile.get("narrative", {})
    primary_color = brand.get("primary_color", "#0f766e")
    secondary_color = brand.get("secondary_color", "#122033")
    accent_soft = brand.get("accent_soft", "#dff7f4")
    hero_gradient_start = brand.get("hero_gradient_start", "#eaf1f8")
    hero_gradient_end = brand.get("hero_gradient_end", "#f4f7fb")

    board_table = pd.DataFrame(
        [
            {"Metric": "Latest Revenue", "Value": summary["latest_revenue_usd"]},
            {"Metric": "NRR", "Value": summary["nrr_latest"]},
            {"Metric": "Gross Churn", "Value": summary["gross_churn_latest"]},
            {"Metric": "Total Value at Risk", "Value": summary["total_value_at_risk_usd"]},
            {"Metric": "Quality Score", "Value": scorecard["overall_score"]},
            {"Metric": "Adoption Rate", "Value": adoption["adoption_rate"]},
            {
                "Metric": "Accepted Recovery Value",
                "Value": adoption.get("accepted_expected_recovery_usd", 0.0),
            },
        ]
    )
    board_table_path = OUTPUT_DIR / "board_summary.csv"
    board_table.to_csv(board_table_path, index=False)

    actions_path = OUTPUT_DIR / "top_actions.csv"
    top_actions.to_csv(actions_path, index=False)

    markdown_path = OUTPUT_DIR / "executive_review_pack.md"
    lines = [
        "# Executive Review Pack",
        "",
        f"Client: {solution_profile.get('client_name', 'n/a')}",
        f"Industry: {solution_profile.get('industry', 'n/a')}",
        f"Package: {solution_profile.get('package', {}).get('name', 'n/a')}",
        "",
        "## Board Summary",
        f"- Latest Revenue: ${summary['latest_revenue_usd']:,.0f}",
        f"- NRR: {summary['nrr_latest']:.1%}",
        f"- Gross Churn: {summary['gross_churn_latest']:.1%}",
        f"- Total Value at Risk: ${summary['total_value_at_risk_usd']:,.0f}",
        f"- Quality Score: {scorecard['overall_score']:.1f}",
        f"- Adoption Rate: {adoption['adoption_rate']:.1%}",
        f"- Accepted Recovery Value: ${adoption.get('accepted_expected_recovery_usd', 0.0):,.0f}",
        "",
        "## Executive Insights",
    ]
    for insight in insights.get("insights", []):
        lines.append(f"- {insight['headline']} {insight['detail']}")
    lines.extend(
        [
            "",
            "## Recommended Actions",
        ]
    )
    for action in insights.get("recommended_actions", []):
        lines.append(
            f"- {action['account_id']}: {action['recommended_action']} | "
            f"risk ${action['revenue_at_risk_usd']:,.0f} | "
            f"recovery ${action['expected_recovery_usd']:,.0f}"
        )
    lines.extend(
        [
            "",
            "## Copyright And Usage",
            "Copyright (c) 2026 Samuel Maia. This executive review pack and its supporting assets are proprietary.",
            "Public viewing does not grant reuse, redistribution, sublicensing, or derivative rights.",
        ]
    )
    markdown_path.write_text("\n".join(lines), encoding="utf-8")

    html_path = OUTPUT_DIR / "executive_review_pack.html"
    insight_items = "".join(
        f"<li><strong>{insight['headline']}</strong><br>{insight['detail']}</li>"
        for insight in insights.get("insights", [])
    )
    action_rows = "".join(
        "<tr>"
        f"<td>{action['account_id']}</td>"
        f"<td>{action['recommended_action']}</td>"
        f"<td>${action['revenue_at_risk_usd']:,.0f}</td>"
        f"<td>${action['expected_recovery_usd']:,.0f}</td>"
        "</tr>"
        for action in insights.get("recommended_actions", [])
    )
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Executive Review Pack</title>
  <style>
    :root {{
      --bg: #f4f7fb;
      --ink: {secondary_color};
      --muted: #5b6b81;
      --card: #ffffff;
      --accent: {primary_color};
      --accent-soft: {accent_soft};
      --warn: #b45309;
    }}
    body {{ margin: 0; font-family: Arial, sans-serif; background: linear-gradient(180deg, {hero_gradient_start} 0%, {hero_gradient_end} 100%); color: var(--ink); }}
    .wrap {{ max-width: 1120px; margin: 0 auto; padding: 40px 24px 64px; }}
    .hero {{ background: var(--card); border-radius: 24px; padding: 32px; box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08); }}
    .hero h1 {{ margin: 0 0 8px; font-size: 38px; }}
    .hero p {{ margin: 0; color: var(--muted); font-size: 18px; }}
    .grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-top: 24px; }}
    .card {{ background: var(--card); border-radius: 20px; padding: 20px; box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06); }}
    .label {{ color: var(--muted); font-size: 13px; text-transform: uppercase; letter-spacing: 0.08em; }}
    .value {{ margin-top: 8px; font-size: 28px; font-weight: 700; }}
    .section {{ margin-top: 28px; }}
    .panel {{ background: var(--card); border-radius: 20px; padding: 24px; box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06); }}
    ul {{ margin: 0; padding-left: 18px; }}
    li {{ margin: 0 0 14px; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ padding: 12px 10px; border-bottom: 1px solid #e5ebf2; text-align: left; }}
    th {{ font-size: 13px; color: var(--muted); text-transform: uppercase; }}
    .pill {{ display: inline-block; padding: 6px 10px; border-radius: 999px; background: var(--accent-soft); color: var(--accent); font-size: 12px; font-weight: 700; }}
    .notice {{ margin-top: 24px; padding: 16px 18px; border-radius: 18px; background: #fff7ed; color: #9a3412; border: 1px solid #fed7aa; font-size: 14px; }}
    .footer {{ margin-top: 28px; color: var(--muted); font-size: 13px; text-align: center; }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="hero">
      <span class="pill">{solution_profile.get('package', {}).get('name', 'Executive Package')}</span>
      <h1>Executive Review Pack</h1>
      <p>{solution_profile.get('client_name', 'n/a')} | {solution_profile.get('industry', 'n/a')} | {solution_profile.get('executive_buyer', 'n/a')}</p>
      <p style="margin-top: 12px;"><strong>{narrative.get('headline', '')}</strong><br>{narrative.get('value_proposition', '')}</p>
    </div>
    <div class="grid">
      <div class="card"><div class="label">Latest Revenue</div><div class="value">${summary['latest_revenue_usd']:,.0f}</div></div>
      <div class="card"><div class="label">NRR</div><div class="value">{summary['nrr_latest']:.1%}</div></div>
      <div class="card"><div class="label">Value At Risk</div><div class="value">${summary['total_value_at_risk_usd']:,.0f}</div></div>
      <div class="card"><div class="label">Quality Score</div><div class="value">{scorecard['overall_score']:.1f}</div></div>
    </div>
    <div class="section panel">
      <h2>Executive Insights</h2>
      <ul>{insight_items}</ul>
    </div>
    <div class="section panel">
      <h2>Realized Outcomes</h2>
      <p>Adoption Rate: <strong>{adoption['adoption_rate']:.1%}</strong> | Accepted Recovery Value: <strong>${adoption.get('accepted_expected_recovery_usd', 0.0):,.0f}</strong></p>
    </div>
    <div class="section panel">
      <h2>Recommended Actions</h2>
      <table>
        <thead><tr><th>Account</th><th>Action</th><th>Revenue At Risk</th><th>Expected Recovery</th></tr></thead>
        <tbody>{action_rows}</tbody>
      </table>
    </div>
    <div class="notice">
      Copyright (c) 2026 Samuel Maia. This executive review pack is provided for evaluation and stakeholder review only.
      Public access does not grant reuse, redistribution, sublicensing, or derivative rights.
    </div>
    <div class="footer">Proprietary analytics product asset | Samuel Maia</div>
  </div>
</body>
</html>"""
    html_path.write_text(html, encoding="utf-8")

    json_path = OUTPUT_DIR / "executive_review_pack.json"
    json_path.write_text(
        json.dumps(
            {
                "solution_profile": solution_profile,
                "summary": summary,
                "scorecard": scorecard,
                "adoption": adoption,
                "insights": insights,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    return {
        "markdown": markdown_path,
        "html": html_path,
        "json": json_path,
        "board_summary": board_table_path,
        "top_actions": actions_path,
    }


def main() -> None:
    outputs = build_pack()
    print("Executive review pack generated:")
    for key, path in outputs.items():
        print(f"- {key}: {path}")


if __name__ == "__main__":
    main()
