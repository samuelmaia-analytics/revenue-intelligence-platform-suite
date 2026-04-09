# GenAI Governance

## Purpose
GenAI in this platform exists to accelerate executive insight drafting, not to replace validated analytics logic.

## Current Implementation
- deterministic fallback generator in `packages/common/executive.py`
- artifact persisted to `reports/showcase/executive_insights.json`
- thresholds, package metadata, and recommendation context stored with the output
- no free-form LLM dependency required for the executive insight layer

## Guardrails
- only validated and contract-backed metrics can feed insight generation
- prompts and generation policy must be versioned and auditable
- business rules remain the source of truth for recommendations
- generated narratives must never bypass governance, owner assignment, or scorecard checks

## Acceptable Use
- draft executive highlights
- summarize KPI movement against thresholds
- recommend operating actions based on validated logic

## Unacceptable Use
- inventing facts not present in validated artifacts
- replacing data contracts or semantic definitions
- generating client-facing claims without traceable metric evidence

## Next Step
If an LLM-backed layer is introduced later, it should inherit the same contract inputs, persist prompt context, and support deterministic fallback for environments where LLM use is not permitted.
