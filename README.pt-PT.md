# Revenue-Intelligence-Platform-Suite

Plataforma unificada de Revenue + Retention Intelligence, consolidando engenharia de dados, analytics e ML num unico monorepo modular.

## Idioma
- English: [README.md](README.md)
- Portugues (BR): [README.pt-BR.md](README.pt-BR.md)
- Portugues (PT): [README.pt-PT.md](README.pt-PT.md)

## Sumario
- [O Que E](#o-que-e)
- [Arquitetura da Plataforma](#arquitetura-da-plataforma)
- [Como os Repositorios Compoem a Plataforma](#como-os-repositorios-compoem-a-plataforma)
- [Modulos](#modulos)
- [Estrutura do Monorepo](#estrutura-do-monorepo)
- [Documentos Executivos](#documentos-executivos)
- [Quickstart](#quickstart)
- [Atualizacao de Subtree](#atualizacao-de-subtree)
- [Resultados de Negocio](#resultados-de-negocio)
- [Stack Tecnologica](#stack-tecnologica)

## O Que E

- Arquitetura em camadas: `raw -> bronze -> silver -> gold`
- Modelos de negocio: churn, next purchase, LTV e priorizacao
- Aplicacoes executivas e operacionais com Streamlit
- Governanca tecnica com contratos de dados, testes e CI

## Arquitetura da Plataforma

```mermaid
flowchart TD
  subgraph Sources["Data Sources"]
    S1[CRM ERP CSV]
    S2[Ecommerce Sales]
    S3[Marketing Spend]
  end

  subgraph Pipeline["Data Platform"]
    I[Ingestion]
    Q[Data Quality - Pandera]
    T[Transforms and Star Schema]
  end

  subgraph ML["ML Layer"]
    M1[Churn Model]
    M2[Next Purchase Model]
    M3[LTV Segmentation]
    R[Recommendation Prioritization]
  end

  subgraph Serving["Serving & Apps"]
    A1[Batch Scoring]
    A2[API FastAPI Optional]
    D1[Executive Streamlit Dashboard]
    D2[Sales Analytics Streamlit]
  end

  Sources --> I --> Q --> T
  T --> M1 --> R --> A1 --> D1
  T --> M2 --> R
  T --> M3 --> R
  A2 --> D1
  A2 --> D2
```

## Como os Repositorios Compoem a Plataforma

```mermaid
flowchart LR
  R1[Revenue-Intelligence-Platform] --> P[Revenue-Intelligence-Platform-Suite]
  R2[churn-prediction] --> P
  R3[amazon-sales-analysis] --> P
  R4[analise-vendas-python] --> P
  R5[data-senior-analytics] --> P
```

## Modulos

| Caminho do Modulo | Repositorio de Origem | Estado |
|---|---|---|
| [modules/revenue-intelligence](./modules/revenue-intelligence) | Revenue-Intelligence-Platform-End-to-End-Analytics-ML-System | Integrado via subtree |
| [modules/churn-prediction](./modules/churn-prediction) | churn-prediction | Integrado via subtree |
| [modules/amazon-sales-analysis](./modules/amazon-sales-analysis) | amazon-sales-analysis | Integrado via subtree |
| [modules/analise-vendas-python](./modules/analise-vendas-python) | analise-vendas-python | Integrado via subtree |
| [modules/data-senior-analytics](./modules/data-senior-analytics) | data-senior-analytics | Integrado via subtree |

## Estrutura do Monorepo

```text
revenue-intelligence-platform-suite/
|- apps/
|- datasets/
|- docs/
|- modules/
|- packages/
|- platform/
|- tests/
`- pyproject.toml
```

## Documentos Executivos

- [Executive Brief](./docs/executive-brief.md)
- [KPI Scorecard](./docs/kpi-scorecard.md)

## Quickstart

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
streamlit run apps/executive-dashboard/app.py
```

## Atualizacao de Subtree

```bash
git fetch churn-prediction main
git subtree pull --prefix modules/churn-prediction churn-prediction main --squash
```

## Resultados de Negocio

- Melhor priorizacao de clientes de elevado valor e elevado risco
- Decisoes mais rapidas para retencao e crescimento de receita
- Reprodutibilidade de pipelines e rastreabilidade de modelos

## Stack Tecnologica

Python, SQL, Streamlit, scikit-learn, Prefect, Pandera, MLflow, Pytest, Docker.
