from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "dist" / "client-microsite"
PROPOSAL_DIR = ROOT / "dist" / "client-proposal-pack"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_client_proposal_pack import main as build_client_proposal_pack  # noqa: E402


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    build_client_proposal_pack()
    proposal = _load_json(PROPOSAL_DIR / "client_proposal.json")
    solution_profile = proposal["solution_profile"]
    brand = solution_profile.get("brand", {})
    narrative = solution_profile.get("narrative", {})
    benchmark = proposal.get("benchmark") or {}
    commercial = proposal.get("commercial_structure", {})

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{proposal.get('proposal_client_name', 'Client')} Microsite</title>
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; background: linear-gradient(180deg, {brand.get('hero_gradient_start', '#eef6ff')} 0%, {brand.get('hero_gradient_end', '#ffffff')} 100%); color: {brand.get('secondary_color', '#122033')}; }}
    .wrap {{ max-width: 1120px; margin: 0 auto; padding: 36px 24px 64px; }}
    .hero, .panel {{ background: #fff; border-radius: 24px; padding: 28px; box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08); }}
    .hero h1 {{ margin: 0 0 8px; font-size: 42px; }}
    .pill {{ display: inline-block; padding: 6px 10px; border-radius: 999px; background: {brand.get('accent_soft', '#dff7f4')}; color: {brand.get('primary_color', '#0f766e')}; font-size: 12px; font-weight: 700; }}
    .grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 20px; }}
    .card {{ background: #fff; border-radius: 20px; padding: 20px; box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06); }}
    .label {{ font-size: 12px; color: #5b6b81; text-transform: uppercase; }}
    .value {{ margin-top: 8px; font-size: 28px; font-weight: 700; }}
    .panel {{ margin-top: 24px; }}
    iframe {{ width: 100%; height: 780px; border: 0; border-radius: 18px; background: #fff; }}
    .notice {{ margin-top: 24px; padding: 16px 18px; border-radius: 18px; background: #fff7ed; color: #9a3412; border: 1px solid #fed7aa; font-size: 14px; }}
    .footer {{ margin-top: 28px; color: #5b6b81; font-size: 13px; text-align: center; }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="hero">
      <span class="pill">{solution_profile.get('package', {}).get('name', 'Client Microsite')}</span>
      <h1>{proposal.get('proposal_client_name', 'Client')}</h1>
      <p><strong>{narrative.get('headline', '')}</strong><br>{narrative.get('value_proposition', '')}</p>
    </div>
    <div class="grid">
      <div class="card"><div class="label">Setup Fee</div><div class="value">{commercial.get('setup_fee', 'n/a')}</div></div>
      <div class="card"><div class="label">Monthly Service</div><div class="value">{commercial.get('monthly_service', 'n/a')}</div></div>
      <div class="card"><div class="label">Timeline</div><div class="value">{commercial.get('timeline', 'n/a')}</div></div>
    </div>
    <div class="panel">
      <h2>Benchmark Snapshot</h2>
      <p>Industry: {benchmark.get('industry', 'n/a')} | Target NRR: {benchmark.get('nrr_target', 0):.0%} | Churn ceiling: {benchmark.get('gross_churn_ceiling', 0):.0%}</p>
    </div>
    <div class="panel">
      <h2>Executive Review Preview</h2>
      <iframe src="../executive-review-pack/executive_review_pack.html" title="Executive Review Pack"></iframe>
    </div>
    <div class="notice">
      Copyright (c) 2026 Samuel Maia. This microsite is a proprietary commercial and executive demonstration surface.
      Public access does not grant reuse, redistribution, sublicensing, or derivative rights.
    </div>
    <div class="footer">Proprietary microsite asset | Samuel Maia</div>
  </div>
</body>
</html>"""
    (OUTPUT_DIR / "index.html").write_text(html, encoding="utf-8")
    print(f"Client microsite generated in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
