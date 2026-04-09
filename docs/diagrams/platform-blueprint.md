# Platform Blueprint Diagram

```mermaid
flowchart LR
  A[Sources] --> B[Ingestion]
  B --> C[Bronze]
  C --> D[Silver]
  D --> E[Gold]
  E --> F[Semantic Metrics]
  F --> G[Executive Insights]
  G --> H[Apps And API]
  H --> I[Action Telemetry]
  I --> J[Governance And Scorecards]
  J --> H
```
