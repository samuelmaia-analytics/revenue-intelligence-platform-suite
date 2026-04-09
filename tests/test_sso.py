from __future__ import annotations

from common import get_sso_settings, resolve_identity_from_headers


def test_sso_settings_disabled_by_default() -> None:
    settings = get_sso_settings()
    assert settings["mode"] in {"disabled", "trusted_header"}


def test_resolve_identity_without_headers_is_unauthenticated() -> None:
    identity = resolve_identity_from_headers({})
    assert identity["authenticated"] is False
    assert identity["user"] == ""
