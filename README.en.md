# Revenue Intelligence Platform Suite

**Language:** `English` · [Português (Brasil)](README.md) · [Português (Portugal)](README.pt-PT.md)

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-CC_BY--NC_4.0-lightgrey.svg)](LICENSE)

A personal portfolio platform connecting ingestion, transformations, governed metrics, quality, observability and executive applications for revenue and retention analysis.

[Open the public demonstration](https://revenue-intelligence-platform.streamlit.app/)

## Capabilities

- Layered data processing and dimensional modeling with Python, SQL and dbt.
- Shared metric definitions and a semantic layer for consistent KPIs.
- Quality checks, data contracts, freshness monitoring and observability.
- Streamlit applications and FastAPI endpoints for executive consumption.
- Customer retention modeling with scikit-learn and MLflow.
- Prefect orchestration, DuckDB/SQLite persistence and Docker Compose execution.
- Documented privacy, retention, RACI and client isolation assumptions.

The portfolio demonstrates implemented capabilities and reproducible artifacts. It does not claim measured financial outcomes achieved for a real client. Governance and GenAI boundaries are documented separately.

## Architecture

Operational sources feed ingestion and Bronze, Silver and Gold processing. Shared metrics support insights, executive applications and action tracking. Contracts, quality checks and observability provide evidence for reviewing those outputs.

[Technical architecture](docs/architecture.md) · [Semantic metric layer](docs/semantic-metric-layer.md)

## Solution packages

- **Revenue Command Center:** executive revenue and priority monitoring.
- **Retention Intelligence:** churn risk and retention prioritization.
- **Executive KPI Governance:** metric definitions, ownership and quality.
- **Commercial Performance Analytics:** commercial performance analysis.

[Solution documentation](docs/solutions/)

## Run locally

Requires Python 3.11 or later. From the repository root:

```bash
make install
make lint
make test
```

Start the demonstration components as needed:

```bash
make showcase
make app
make api
```

For the local container stack, use `make demo-stack`. See [Docker Compose instructions](docs/docker-compose.md).

## Governance and generated insights

The insights layer works with controlled metrics and rules, a deterministic fallback and persisted review artifacts. Generative AI supports interpretation alongside quality and governance controls.

- [GenAI governance](docs/genai-governance.md)
- [Privacy and LGPD policy](docs/privacy-and-lgpd-policy.md)
- [Governance responsibilities](docs/governance-raci.md)
- [Evidence and proof](docs/proof.md)
- [Documentation index](docs/README.md)

## Author

**Samuel de Andrade Maia — Data Engineer (Pleno) | Analytics Engineer**

Data Engineering at **Avanade** since **20 October 2026**. This is an independent personal portfolio project; it does not represent work, data or results delivered for Avanade or its clients.

[LinkedIn](https://www.linkedin.com/in/samuelmaia-analytics/) · [Portfolio](https://samuelmaia-analytics.github.io/samuelmaia-analytics/)

## License

**Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**. See [LICENSE](LICENSE) for the full terms.
