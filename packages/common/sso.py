from __future__ import annotations

import os
from collections.abc import Mapping
from typing import Any


def get_sso_settings() -> dict[str, Any]:
    required_groups = [
        group.strip()
        for group in os.getenv("PLATFORM_SSO_REQUIRED_GROUPS", "").split(",")
        if group.strip()
    ]
    return {
        "enabled": os.getenv("PLATFORM_SSO_MODE", "disabled").strip().lower() == "trusted_header",
        "mode": os.getenv("PLATFORM_SSO_MODE", "disabled").strip().lower(),
        "user_header": os.getenv("PLATFORM_SSO_HEADER_USER", "x-auth-request-email").strip().lower(),
        "name_header": os.getenv("PLATFORM_SSO_HEADER_NAME", "x-auth-request-user").strip().lower(),
        "groups_header": os.getenv("PLATFORM_SSO_HEADER_GROUPS", "x-auth-request-groups")
        .strip()
        .lower(),
        "required_groups": required_groups,
    }


def _normalize_headers(headers: Mapping[str, str] | None) -> dict[str, str]:
    if not headers:
        return {}
    return {str(key).lower(): str(value) for key, value in headers.items()}


def resolve_identity_from_headers(headers: Mapping[str, str] | None) -> dict[str, Any]:
    settings = get_sso_settings()
    normalized = _normalize_headers(headers)
    user = normalized.get(settings["user_header"], "").strip()
    display_name = normalized.get(settings["name_header"], "").strip()
    raw_groups = normalized.get(settings["groups_header"], "").strip()
    groups = [group.strip() for group in raw_groups.split(",") if group.strip()]
    required_groups = settings["required_groups"]
    authorized = True if not required_groups else any(group in groups for group in required_groups)
    return {
        "sso_enabled": settings["enabled"],
        "mode": settings["mode"],
        "authenticated": bool(user),
        "authorized": bool(user) and authorized if settings["enabled"] else True,
        "user": user,
        "display_name": display_name or user,
        "groups": groups,
        "required_groups": required_groups,
    }


def get_streamlit_headers(st_module: Any) -> dict[str, str]:
    context = getattr(st_module, "context", None)
    headers = getattr(context, "headers", None)
    if not headers:
        return {}
    try:
        return dict(headers)
    except Exception:
        return {}


def enforce_streamlit_sso(st_module: Any) -> dict[str, Any]:
    identity = resolve_identity_from_headers(get_streamlit_headers(st_module))
    if not identity["sso_enabled"]:
        return identity
    if not identity["authenticated"]:
        st_module.error(
            "Single sign-on is required for this environment. Route this app through the identity-aware proxy."
        )
        st_module.stop()
    if not identity["authorized"]:
        st_module.error("Authenticated user is missing one of the required SSO groups for this app.")
        st_module.stop()
    return identity
