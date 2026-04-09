# ADR 0002: Privacy And Client Data Governance Baseline

- Status: Accepted
- Date: 2026-04-08

## Context

The platform is designed to support analytics delivery for multiple clients, including executive dashboards, proposal assets, deal rooms, and go-to-market exports. That creates a risk of inconsistent privacy handling unless repository-level controls are made explicit.

## Decision

Adopt a repository-level privacy and client data governance baseline with the following requirements:
- no raw personal data committed to the repository
- anonymized, synthetic, or sanitized data only for showcase and CI usage
- client onboarding requires legal basis, owner registration, and retention policy definition
- client-facing artifacts must exclude raw personal or sensitive records by default
- governance controls must be checked in CI alongside code and artifact validation

## Consequences

- Positive:
  - stronger LGPD and privacy posture for client-facing work
  - clearer onboarding expectations for analytics delivery
  - better alignment between engineering, governance, and commercial operations
- Negative:
  - more documentation and review overhead during onboarding
  - stricter requirements before loading operational client data

## Follow-up

- maintain privacy policy and compliance checklist as living controls
- review data retention matrix during client onboarding
- require DPA and usage template review for operational deployments
