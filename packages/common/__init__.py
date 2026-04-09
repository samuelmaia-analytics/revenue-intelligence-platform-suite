"""Shared utilities for all modules."""

from .approvals import build_approval_workflow, load_approval_overrides
from .configuration import list_client_profiles, load_solution_configuration
from .executive import (
    build_data_quality_scorecard,
    build_recommended_actions,
    build_solution_profile,
    generate_executive_insight_report,
    get_solution_packages,
)
from .secrets import build_tenant_secret_status, load_tenant_secret_template, load_tenant_secrets
from .semantic_metrics import get_semantic_metric, list_semantic_metrics, load_semantic_metric_catalog
from .sso import enforce_streamlit_sso, get_sso_settings, resolve_identity_from_headers

__all__ = [
    "build_data_quality_scorecard",
    "build_approval_workflow",
    "build_recommended_actions",
    "build_solution_profile",
    "load_approval_overrides",
    "generate_executive_insight_report",
    "get_solution_packages",
    "build_tenant_secret_status",
    "list_client_profiles",
    "load_tenant_secret_template",
    "load_tenant_secrets",
    "load_solution_configuration",
    "get_semantic_metric",
    "list_semantic_metrics",
    "load_semantic_metric_catalog",
    "enforce_streamlit_sso",
    "get_sso_settings",
    "resolve_identity_from_headers",
]
