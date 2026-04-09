from __future__ import annotations

import importlib.util
import os
from pathlib import Path

from fastapi.testclient import TestClient

from apps.executive_api.main import app


client = TestClient(app)


def _load_module(root: Path, relative_script: str, module_name: str):
    script_path = root / relative_script
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Could not load module from {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_health_endpoint_is_available() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert "artifacts_ready" in payload
    assert "sso" in payload


def test_profiles_endpoint_lists_available_profiles() -> None:
    response = client.get("/profiles")
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["profiles"]) >= 3


def test_profile_secret_status_endpoint_returns_masked_status() -> None:
    response = client.get("/profiles/saas_b2b/secret-status?deployment_env=showcase")
    assert response.status_code == 200
    payload = response.json()
    assert payload["profile_id"] == "saas_b2b"
    assert "checks" in payload
    assert "secrets" not in payload


def test_auth_config_endpoint_returns_sso_settings() -> None:
    response = client.get("/auth/config")
    assert response.status_code == 200
    payload = response.json()
    assert "mode" in payload


def test_auth_me_endpoint_returns_identity_snapshot() -> None:
    response = client.get("/auth/me")
    assert response.status_code == 200
    payload = response.json()
    assert "authenticated" in payload


def test_sso_blocks_api_without_trusted_headers_when_enabled() -> None:
    original_mode = os.environ.get("PLATFORM_SSO_MODE")
    os.environ["PLATFORM_SSO_MODE"] = "trusted_header"
    try:
        response = client.get("/profiles")
        assert response.status_code == 401
    finally:
        if original_mode is None:
            os.environ.pop("PLATFORM_SSO_MODE", None)
        else:
            os.environ["PLATFORM_SSO_MODE"] = original_mode


def test_sso_blocks_api_when_required_group_is_missing() -> None:
    original_mode = os.environ.get("PLATFORM_SSO_MODE")
    original_groups = os.environ.get("PLATFORM_SSO_REQUIRED_GROUPS")
    os.environ["PLATFORM_SSO_MODE"] = "trusted_header"
    os.environ["PLATFORM_SSO_REQUIRED_GROUPS"] = "analytics-admin"
    try:
        response = client.get(
            "/profiles",
            headers={
                "X-Auth-Request-Email": "user@example.com",
                "X-Auth-Request-User": "Example User",
                "X-Auth-Request-Groups": "executive-viewer",
            },
        )
        assert response.status_code == 403
    finally:
        if original_mode is None:
            os.environ.pop("PLATFORM_SSO_MODE", None)
        else:
            os.environ["PLATFORM_SSO_MODE"] = original_mode
        if original_groups is None:
            os.environ.pop("PLATFORM_SSO_REQUIRED_GROUPS", None)
        else:
            os.environ["PLATFORM_SSO_REQUIRED_GROUPS"] = original_groups


def test_sso_allows_api_with_trusted_headers_and_required_group() -> None:
    original_mode = os.environ.get("PLATFORM_SSO_MODE")
    original_groups = os.environ.get("PLATFORM_SSO_REQUIRED_GROUPS")
    os.environ["PLATFORM_SSO_MODE"] = "trusted_header"
    os.environ["PLATFORM_SSO_REQUIRED_GROUPS"] = "analytics-admin"
    try:
        response = client.get(
            "/profiles",
            headers={
                "X-Auth-Request-Email": "user@example.com",
                "X-Auth-Request-User": "Example User",
                "X-Auth-Request-Groups": "analytics-admin,executive-viewer",
            },
        )
        assert response.status_code == 200
    finally:
        if original_mode is None:
            os.environ.pop("PLATFORM_SSO_MODE", None)
        else:
            os.environ["PLATFORM_SSO_MODE"] = original_mode
        if original_groups is None:
            os.environ.pop("PLATFORM_SSO_REQUIRED_GROUPS", None)
        else:
            os.environ["PLATFORM_SSO_REQUIRED_GROUPS"] = original_groups


def test_semantic_metrics_endpoint_returns_catalog() -> None:
    response = client.get("/semantic-metrics")
    assert response.status_code == 200
    payload = response.json()
    assert payload["catalog_version"] == "1.0.0"


def test_executive_summary_endpoint_returns_showcase_payload() -> None:
    response = client.get("/executive/summary")
    assert response.status_code == 200
    payload = response.json()
    assert "latest_month" in payload


def test_executive_review_pack_endpoint_returns_payload_when_generated() -> None:
    root = Path(__file__).resolve().parents[1]
    review_pack_module = _load_module(
        root, "scripts/build_executive_review_pack.py", "build_executive_review_pack_for_api"
    )
    review_pack_module.build_pack()
    response = client.get("/executive/review-pack")
    assert response.status_code == 200
    payload = response.json()
    assert "summary" in payload


def test_executive_review_pack_html_endpoint_returns_path() -> None:
    response = client.get("/executive/review-pack/html")
    assert response.status_code == 200
    payload = response.json()
    assert payload["exists"] is True


def test_executive_proposal_pack_endpoint_returns_payload_when_generated() -> None:
    root = Path(__file__).resolve().parents[1]
    proposal_module = _load_module(
        root, "scripts/build_client_proposal_pack.py", "build_client_proposal_pack_for_api"
    )
    proposal_module.main()
    response = client.get("/executive/proposal-pack")
    assert response.status_code == 200
    payload = response.json()
    assert "solution_profile" in payload


def test_executive_microsite_endpoint_returns_path_when_generated() -> None:
    root = Path(__file__).resolve().parents[1]
    microsite_module = _load_module(root, "scripts/build_client_microsite.py", "build_client_microsite_for_api")
    microsite_module.main()
    response = client.get("/executive/microsite")
    assert response.status_code == 200
    payload = response.json()
    assert payload["exists"] is True


def test_executive_deal_room_endpoint_returns_manifest_when_generated() -> None:
    root = Path(__file__).resolve().parents[1]
    deal_module = _load_module(root, "scripts/build_deal_room.py", "build_deal_room_for_api")
    deal_module.main()
    response = client.get("/executive/deal-room/flagship-client")
    assert response.status_code == 200
    payload = response.json()
    assert payload["room_slug"] == "flagship-client"


def test_executive_deal_room_approvals_endpoint_returns_workflow_when_generated() -> None:
    root = Path(__file__).resolve().parents[1]
    module = _load_module(root, "scripts/build_formal_approval_pack.py", "build_formal_approval_pack_for_api")
    module.main()
    response = client.get("/executive/deal-room/flagship-client/approvals")
    assert response.status_code == 200
    payload = response.json()
    assert payload["stage_count"] == 4


def test_executive_deal_room_publication_endpoint_returns_manifest_when_generated() -> None:
    root = Path(__file__).resolve().parents[1]
    module = _load_module(
        root, "scripts/build_external_publication_bundle.py", "build_external_publication_bundle_for_api"
    )
    module.main()
    response = client.get("/executive/deal-room/flagship-client/publication")
    assert response.status_code == 200
    payload = response.json()
    assert payload["room_slug"] == "flagship-client"


def test_executive_sales_bundle_endpoint_returns_payload_when_generated() -> None:
    root = Path(__file__).resolve().parents[1]
    bundle_module = _load_module(
        root, "scripts/build_sales_enablement_bundle.py", "build_sales_enablement_bundle_for_api"
    )
    bundle_module.main()
    response = client.get("/executive/sales-bundle/flagship-client")
    assert response.status_code == 200
    payload = response.json()
    assert payload["deal_name"] == "Flagship Client"


def test_executive_gtm_export_endpoint_returns_payload_when_generated() -> None:
    root = Path(__file__).resolve().parents[1]
    module = _load_module(root, "scripts/build_gtm_exports.py", "build_gtm_exports_for_api")
    module.main()
    response = client.get("/executive/gtm-export/flagship-client/hubspot_deal_payload")
    assert response.status_code == 200
    payload = response.json()
    assert "properties" in payload
