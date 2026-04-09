from __future__ import annotations

from common import build_tenant_secret_status, load_tenant_secret_template, load_tenant_secrets


def test_load_tenant_secret_template_contains_required_layers() -> None:
    template = load_tenant_secret_template(client_profile="saas_b2b", deployment_env="showcase")
    assert template["crm"]["api_token"] == "__required__"
    assert template["runtime"]["streamlit_cookie_secret"] == "__required__"
    assert template["connectors"]["stripe_api_key"] == "__required__"


def test_load_tenant_secrets_returns_maskable_structure_without_live_values() -> None:
    resolved = load_tenant_secrets(client_profile="saas_b2b", deployment_env="showcase")
    assert "secrets" in resolved
    assert "loaded_sources" in resolved
    assert "source_map" in resolved


def test_build_tenant_secret_status_reports_missing_keys_without_values() -> None:
    status = build_tenant_secret_status(client_profile="saas_b2b", deployment_env="showcase")
    assert status["required_secret_count"] >= 1
    assert status["configured_secret_count"] == 0
    assert status["ready"] is False
    assert status["missing_secret_count"] == status["required_secret_count"]
    assert all("secret_key" in check and "configured" in check for check in status["checks"])
