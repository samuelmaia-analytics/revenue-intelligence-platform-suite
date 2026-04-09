# Architecture

## Executive Intent
The platform is designed as a reusable analytics operating system for clients that need trusted revenue, retention, and commercial decision support. The goal is not only to model data correctly, but to turn it into an executive workflow with governance, action prioritization, and recurring service delivery.

## Enterprise Blueprint
```text
sources -> ingestion -> bronze -> silver -> gold -> semantic metrics -> executive insights -> apps -> action telemetry
                                              \-> quality + freshness + contracts -> scorecards -> governance
```

Reusable visual version: [docs/diagrams/platform-blueprint.md](./diagrams/platform-blueprint.md)

![Platform blueprint](./assets/platform-blueprint.svg)

## Logical Layers

### 1. Ingestion and Connector Layer
- `platform/ingestion`
- `platform_connectors`
- `platform/connectors`

Responsibilities:
- abstract source access
- normalize telemetry ingestion
- support local demo backends and future enterprise connectors
- allow client-specific connector expansion without changing the executive layer

### 2. Transformation Layer
- `platform/transform`
- `modules/revenue-intelligence/src/transform`
- dbt project in `modules/revenue-intelligence/dbt`

Responsibilities:
- separate raw, validated, and curated transformations
- implement `bronze`, `silver`, and `gold` style promotion
- keep business logic traceable from source to executive KPI

### 3. Semantic and Business Metric Layer
- `modules/revenue-intelligence/src/analytics/semantic_layer.py`
- `packages/common`

Responsibilities:
- standardize KPI definitions
- decouple business metric logic from app rendering
- support consistent metric meaning across clients and industries

### 4. Modeling and Recommendation Layer
- `platform/modeling`
- `modules/revenue-intelligence/src/models`
- `modules/revenue-intelligence/src/recommendation.py`

Responsibilities:
- risk scoring and predictive models
- action prioritization logic
- scenario planning inputs for executive decisions

### 5. Observability and Governance Layer
- `platform_observability`
- `packages/common/contracts`
- generated showcase scorecards in `reports/showcase`

Responsibilities:
- contract validation
- drift and adoption monitoring
- freshness and quality scorecards
- executive evidence artifacts for release and governance reviews

### 6. Serving and Experience Layer
- `apps/executive-dashboard`
- `apps/sales-analytics`
- module-level Streamlit applications

Responsibilities:
- executive and operational consumption
- story-driven KPI hierarchy
- recommended action presentation
- white-label presentation surface

## Architectural Gaps Identified In The Audit
- connector namespaces are duplicated between `platform/*` and `platform_connectors/*`
- client-level configuration is implied, but not yet centralized at the root platform layer
- root contracts cover showcase outputs, but business contracts can be expanded by domain and version
- quality and freshness signals existed operationally, but were not surfaced clearly as executive assets
- README and docs communicated maturity, but not yet in a directly sellable packaging format

## Improvements Implemented
- added reusable executive productization utilities in `packages/common/executive.py`
- added root `config/` hierarchy for environment, client, and solution-package layering
- added generated `solution_profile`, `data_quality_scorecard`, and `executive_insights` artifacts
- upgraded the flagship app to expose package framing, executive narrative, recommended actions, and scorecards
- added FastAPI serving layer in `apps/executive_api`
- created commercial and solution-package documentation for productized delivery

## Recommended Next Architectural Moves

### Near-term
- add versioned business contracts for source, metric, and executive payloads
- define a stable compatibility layer for connector registration by client

### Mid-term
- extend Docker Compose with managed storage and monitoring services
- promote semantic metrics into explicit dbt or metric-spec artifacts

### Later
- introduce multi-tenant artifact namespaces
- connect realized outcome telemetry back to action ROI attribution
- formalize release artifact validation and evidence packaging in CI
