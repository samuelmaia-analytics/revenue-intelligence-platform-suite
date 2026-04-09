from __future__ import annotations

import json
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse


def _find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "pyproject.toml").exists() and (candidate / "packages").exists():
            return candidate
    return Path(__file__).resolve().parents[2]


ROOT = _find_repo_root(Path(__file__).resolve())
try:
    import common  # noqa: F401
except ModuleNotFoundError:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    if str(ROOT / "packages") not in sys.path:
        sys.path.insert(0, str(ROOT / "packages"))

from common import (  # noqa: E402
    build_tenant_secret_status,
    get_sso_settings,
    list_client_profiles,
    load_semantic_metric_catalog,
    resolve_identity_from_headers,
)
from common.configuration import load_solution_configuration  # noqa: E402

app = FastAPI(
    title="Revenue Intelligence Executive API",
    version="1.1.0",
    description=(
        "Serving layer for executive summary, scorecards, insights, and client adaptation profiles. "
        "This API and its generated executive assets are proprietary to Samuel Maia. "
        "Public documentation or runtime access does not grant reuse, redistribution, or sublicensing rights."
    ),
    contact={"name": "Samuel Maia"},
    license_info={"name": "Proprietary - All rights reserved"},
)

SHOWCASE_DIR = ROOT / "reports" / "showcase"
DIST_DIR = ROOT / "dist" / "executive-review-pack"
PROPOSAL_DIR = ROOT / "dist" / "client-proposal-pack"
MICROSITE_DIR = ROOT / "dist" / "client-microsite"
DEAL_ROOMS_DIR = ROOT / "dist" / "deal-rooms"
PUBLIC_PATH_PREFIXES = {"/health", "/docs", "/openapi.json", "/redoc"}


@app.middleware("http")
async def enforce_api_sso(request: Request, call_next):
    if any(
        request.url.path == public_path or request.url.path.startswith(f"{public_path}/")
        for public_path in PUBLIC_PATH_PREFIXES
    ):
        return await call_next(request)
    identity = resolve_identity_from_headers(request.headers)
    request.state.identity = identity
    if identity["sso_enabled"] and not identity["authenticated"]:
        return JSONResponse(
            status_code=401,
            content={"detail": "SSO required. Provide trusted identity headers from the configured proxy."},
        )
    if identity["sso_enabled"] and not identity["authorized"]:
        return JSONResponse(
            status_code=403,
            content={"detail": "Authenticated identity is not authorized for this API."},
        )
    return await call_next(request)


def _load_json_artifact(file_name: str) -> dict:
    path = SHOWCASE_DIR / file_name
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Artifact not found: {file_name}")
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


@app.get("/health")
def health() -> dict:
    tenant_secret_status_path = SHOWCASE_DIR / "tenant_secret_status.json"
    return {
        "status": "ok",
        "artifacts_ready": all(
            (SHOWCASE_DIR / name).exists()
            for name in [
                "summary.json",
                "solution_profile.json",
                "data_quality_scorecard.json",
                "executive_insights.json",
            ]
        ),
        "tenant_secret_status_ready": tenant_secret_status_path.exists(),
        "sso": get_sso_settings(),
    }


@app.get("/profiles")
def profiles() -> dict:
    return {"profiles": list_client_profiles()}


@app.get("/semantic-metrics")
def semantic_metrics() -> dict:
    return load_semantic_metric_catalog()


@app.get("/profiles/{profile_id}")
def profile(profile_id: str, solution_package: str = "revenue_command_center") -> dict:
    return load_solution_configuration(
        client_profile=profile_id,
        deployment_env="showcase",
        solution_package=solution_package,
    )


@app.get("/profiles/{profile_id}/secret-status")
def profile_secret_status(profile_id: str, deployment_env: str = "showcase") -> dict:
    return build_tenant_secret_status(
        client_profile=profile_id,
        deployment_env=deployment_env,
    )


@app.get("/auth/config")
def auth_config() -> dict:
    settings = get_sso_settings()
    return {
        "enabled": settings["enabled"],
        "mode": settings["mode"],
        "required_groups": settings["required_groups"],
        "trusted_headers": [
            settings["user_header"],
            settings["name_header"],
            settings["groups_header"],
        ],
    }


@app.get("/auth/me")
def auth_me(request: Request) -> dict:
    identity = getattr(request.state, "identity", resolve_identity_from_headers(request.headers))
    return {
        "authenticated": identity["authenticated"],
        "authorized": identity["authorized"],
        "user": identity["user"],
        "display_name": identity["display_name"],
        "groups": identity["groups"],
        "sso_enabled": identity["sso_enabled"],
    }


@app.get("/executive/summary")
def executive_summary() -> dict:
    return _load_json_artifact("summary.json")


@app.get("/executive/scorecard")
def executive_scorecard() -> dict:
    return _load_json_artifact("data_quality_scorecard.json")


@app.get("/executive/insights")
def executive_insights() -> dict:
    return _load_json_artifact("executive_insights.json")


@app.get("/executive/solution-profile")
def executive_solution_profile() -> dict:
    return _load_json_artifact("solution_profile.json")


@app.get("/executive/review-pack")
def executive_review_pack() -> dict:
    path = DIST_DIR / "executive_review_pack.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Executive review pack not generated.")
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


@app.get("/executive/review-pack/html")
def executive_review_pack_html() -> dict:
    path = DIST_DIR / "executive_review_pack.html"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Executive review pack HTML not generated.")
    return {"path": str(path), "exists": True}


@app.get("/executive/proposal-pack")
def executive_proposal_pack() -> dict:
    path = PROPOSAL_DIR / "client_proposal.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Client proposal pack not generated.")
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


@app.get("/executive/microsite")
def executive_microsite() -> dict:
    path = MICROSITE_DIR / "index.html"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Client microsite not generated.")
    return {"path": str(path), "exists": True}


@app.get("/executive/deal-room/{deal_slug}")
def executive_deal_room(deal_slug: str) -> dict:
    manifest_path = DEAL_ROOMS_DIR / deal_slug / "manifest.json"
    if not manifest_path.exists():
        raise HTTPException(status_code=404, detail="Deal room not generated.")
    with manifest_path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


@app.get("/executive/deal-room/{deal_slug}/approvals")
def executive_deal_room_approvals(deal_slug: str) -> dict:
    path = DEAL_ROOMS_DIR / deal_slug / "approvals" / "approval_workflow.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Approval workflow not generated.")
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


@app.get("/executive/deal-room/{deal_slug}/publication")
def executive_deal_room_publication(deal_slug: str) -> dict:
    path = DEAL_ROOMS_DIR / deal_slug / "publication" / "publication_manifest.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Publication bundle not generated.")
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


@app.get("/executive/sales-bundle/{deal_slug}")
def executive_sales_bundle(deal_slug: str) -> dict:
    path = DEAL_ROOMS_DIR / deal_slug / "sales-enablement" / "crm_handoff.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Sales enablement bundle not generated.")
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


@app.get("/executive/gtm-export/{deal_slug}/{export_name}")
def executive_gtm_export(deal_slug: str, export_name: str) -> dict:
    path = DEAL_ROOMS_DIR / deal_slug / "sales-enablement" / "exports" / f"{export_name}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="GTM export not generated.")
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)
