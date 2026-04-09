from __future__ import annotations

from common import list_client_profiles, load_solution_configuration


def test_list_client_profiles_returns_expected_profiles() -> None:
    profiles = list_client_profiles()
    profile_ids = {profile["profile_id"] for profile in profiles}
    assert {"saas_b2b", "healthtech_growth", "retail_omnichannel"}.issubset(profile_ids)


def test_load_solution_configuration_merges_layers() -> None:
    config = load_solution_configuration(
        client_profile="healthtech_growth",
        deployment_env="showcase",
        solution_package="retention_intelligence",
    )
    assert config["environment_name"] == "showcase"
    assert config["industry"] == "Healthtech"
    assert config["solution_package"]["package_id"] == "retention_intelligence"
    assert config["defaults"]["telemetry_backend"] == "sqlite"
