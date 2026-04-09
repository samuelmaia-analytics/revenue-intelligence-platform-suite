from __future__ import annotations

import json
import os
from typing import Any


DEFAULT_APPROVAL_STAGES = [
    {
        "stage_id": "commercial_review",
        "stage_name": "Commercial Review",
        "required_role": "Account Lead / Solution Lead",
        "owner_team": "Commercial",
        "evidence_required": ["client_proposal.html", "client_proposal.json"],
    },
    {
        "stage_id": "privacy_review",
        "stage_name": "Privacy And LGPD Review",
        "required_role": "Privacy / Legal",
        "owner_team": "Governance",
        "evidence_required": ["client-data-onboarding-template.md", "tenant_secret_status.json"],
    },
    {
        "stage_id": "technical_readiness",
        "stage_name": "Technical Readiness Review",
        "required_role": "Analytics Engineering / Platform",
        "owner_team": "Delivery",
        "evidence_required": ["executive_review_pack.json", "release-evidence-pack"],
    },
    {
        "stage_id": "executive_signoff",
        "stage_name": "Executive Sponsor Sign-off",
        "required_role": "Executive Sponsor",
        "owner_team": "Client Leadership",
        "evidence_required": ["executive_review_pack.html", "microsite.html"],
    },
]


def load_approval_overrides() -> dict[str, dict[str, Any]]:
    raw = os.getenv("APPROVAL_SIGNOFFS", "").strip()
    if not raw:
        return {}
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError("APPROVAL_SIGNOFFS must be valid JSON.") from exc
    if not isinstance(payload, dict):
        raise ValueError("APPROVAL_SIGNOFFS must be a JSON object keyed by stage_id.")
    return {str(key): value for key, value in payload.items() if isinstance(value, dict)}


def build_approval_workflow(
    *,
    deal_name: str,
    proposal_client_name: str,
    artifact_version: str,
    release_tag: str,
    approval_overrides: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    overrides = approval_overrides or {}
    stages: list[dict[str, Any]] = []
    approved_count = 0

    for template in DEFAULT_APPROVAL_STAGES:
        stage = dict(template)
        override = overrides.get(stage["stage_id"], {})
        status = str(override.get("status", "pending")).strip().lower() or "pending"
        approver_name = override.get("approver_name")
        decision_at = override.get("decision_at")
        notes = override.get("notes", "")
        approved = status == "approved"
        if approved:
            approved_count += 1
        stage.update(
            {
                "status": status,
                "approved": approved,
                "approver_name": approver_name,
                "decision_at": decision_at,
                "notes": notes,
            }
        )
        stages.append(stage)

    total_stages = len(stages)
    return {
        "deal_name": deal_name,
        "proposal_client_name": proposal_client_name,
        "artifact_version": artifact_version,
        "release_tag": release_tag,
        "stage_count": total_stages,
        "approved_stage_count": approved_count,
        "pending_stage_count": total_stages - approved_count,
        "ready_for_client_delivery": approved_count == total_stages,
        "stages": stages,
    }
