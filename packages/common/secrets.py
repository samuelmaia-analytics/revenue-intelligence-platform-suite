from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from .configuration import deep_merge


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _secrets_root() -> Path:
    return _repo_root() / "config" / "secrets"


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def _parse_env_value(raw: str) -> Any:
    lowered = raw.strip().lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def _set_nested_value(target: dict[str, Any], path_parts: list[str], value: Any) -> None:
    current = target
    for part in path_parts[:-1]:
        current = current.setdefault(part, {})
    current[path_parts[-1]] = value


def _flatten_dict(data: dict[str, Any], prefix: str = "") -> dict[str, Any]:
    flattened: dict[str, Any] = {}
    for key, value in data.items():
        path = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            flattened.update(_flatten_dict(value, path))
        else:
            flattened[path] = value
    return flattened


def _collect_env_secret_overrides() -> tuple[dict[str, Any], dict[str, str]]:
    overrides: dict[str, Any] = {}
    source_map: dict[str, str] = {}
    prefix = "TENANT_SECRET__"
    for name, raw_value in os.environ.items():
        if not name.startswith(prefix):
            continue
        parts = [part.strip().lower() for part in name[len(prefix) :].split("__") if part.strip()]
        if not parts:
            continue
        value = _parse_env_value(raw_value)
        _set_nested_value(overrides, parts, value)
        source_map[".".join(parts)] = f"env:{name}"
    return overrides, source_map


def _load_layers(paths: list[Path]) -> tuple[dict[str, Any], list[str], dict[str, str]]:
    merged: dict[str, Any] = {}
    loaded_sources: list[str] = []
    source_map: dict[str, str] = {}
    for path in paths:
        if not path.exists():
            continue
        payload = _load_json(path)
        merged = deep_merge(merged, payload)
        loaded_sources.append(str(path.relative_to(_repo_root())))
        for key in _flatten_dict(payload):
            source_map[key] = str(path.relative_to(_repo_root()))
    return merged, loaded_sources, source_map


def load_tenant_secret_template(
    client_profile: str = "saas_b2b",
    deployment_env: str = "showcase",
) -> dict[str, Any]:
    root = _secrets_root() / "templates"
    paths = [
        root / "global.template.json",
        root / "environments" / f"{deployment_env}.template.json",
        root / "clients" / f"{client_profile}.template.json",
    ]
    template, _, _ = _load_layers(paths)
    return template


def load_tenant_secrets(
    client_profile: str = "saas_b2b",
    deployment_env: str = "showcase",
) -> dict[str, Any]:
    root = _secrets_root()
    paths = [
        root / "global.json",
        root / "environments" / f"{deployment_env}.json",
        root / "clients" / f"{client_profile}.json",
        root / "tenants" / deployment_env / f"{client_profile}.json",
    ]
    secrets, loaded_sources, source_map = _load_layers(paths)
    env_overrides, env_source_map = _collect_env_secret_overrides()
    if env_overrides:
        secrets = deep_merge(secrets, env_overrides)
        source_map.update(env_source_map)
        loaded_sources.append("env:TENANT_SECRET__*")

    return {
        "secrets": secrets,
        "loaded_sources": loaded_sources,
        "source_map": source_map,
    }


def build_tenant_secret_status(
    client_profile: str = "saas_b2b",
    deployment_env: str = "showcase",
) -> dict[str, Any]:
    template = load_tenant_secret_template(
        client_profile=client_profile,
        deployment_env=deployment_env,
    )
    resolved = load_tenant_secrets(
        client_profile=client_profile,
        deployment_env=deployment_env,
    )
    template_keys = sorted(_flatten_dict(template).keys())
    secret_keys = _flatten_dict(resolved["secrets"])

    checks: list[dict[str, Any]] = []
    configured = 0
    missing_keys: list[str] = []
    for key in template_keys:
        is_configured = key in secret_keys and secret_keys[key] not in {"", None}
        if is_configured:
            configured += 1
        else:
            missing_keys.append(key)
        checks.append(
            {
                "secret_key": key,
                "configured": is_configured,
                "source": resolved["source_map"].get(key, "missing"),
            }
        )

    return {
        "profile_id": client_profile,
        "deployment_env": deployment_env,
        "required_secret_count": len(template_keys),
        "configured_secret_count": configured,
        "missing_secret_count": len(missing_keys),
        "completeness_ratio": 1.0 if not template_keys else round(configured / len(template_keys), 4),
        "ready": len(missing_keys) == 0,
        "loaded_sources": resolved["loaded_sources"],
        "missing_secret_keys": missing_keys,
        "checks": checks,
    }
