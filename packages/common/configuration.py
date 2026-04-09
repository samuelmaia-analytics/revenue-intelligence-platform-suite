from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _config_root() -> Path:
    return _repo_root() / "config"


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def list_client_profiles() -> list[dict[str, Any]]:
    profiles_dir = _config_root() / "clients"
    profiles: list[dict[str, Any]] = []
    for path in sorted(profiles_dir.glob("*.json")):
        profile = _load_json(path)
        profile["profile_id"] = path.stem
        profiles.append(profile)
    return profiles


def load_solution_configuration(
    client_profile: str = "saas_b2b",
    deployment_env: str = "showcase",
    solution_package: str = "revenue_command_center",
) -> dict[str, Any]:
    root = _config_root()
    global_config = _load_json(root / "global.json")
    environment_config = _load_json(root / "environments" / f"{deployment_env}.json")
    client_config = _load_json(root / "clients" / f"{client_profile}.json")
    package_config = _load_json(root / "solution_packages" / f"{solution_package}.json")
    proposal_defaults = _load_json(root / "proposal_defaults.json")

    config = deep_merge(global_config, environment_config)
    config = deep_merge(config, client_config)
    config = deep_merge(config, proposal_defaults)
    config = deep_merge(config, {"solution_package": package_config})
    config["profile_id"] = client_profile
    config["deployment_env"] = deployment_env
    return config
