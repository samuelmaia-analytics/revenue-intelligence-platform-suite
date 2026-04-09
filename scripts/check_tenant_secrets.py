from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "packages") not in sys.path:
    sys.path.insert(0, str(ROOT / "packages"))

from common.secrets import build_tenant_secret_status  # noqa: E402


def main() -> None:
    client_profile = os.getenv("CLIENT_PROFILE", "saas_b2b").strip().lower()
    deployment_env = os.getenv("DEPLOYMENT_ENV", "showcase").strip().lower()
    strict = os.getenv("REQUIRE_TENANT_SECRETS", "0").strip() == "1"

    status = build_tenant_secret_status(
        client_profile=client_profile,
        deployment_env=deployment_env,
    )
    print(json.dumps(status, indent=2))

    if strict and not status["ready"]:
        raise SystemExit(
            "Tenant secrets validation failed in strict mode. "
            f"Missing keys: {status['missing_secret_keys']}"
        )


if __name__ == "__main__":
    main()
