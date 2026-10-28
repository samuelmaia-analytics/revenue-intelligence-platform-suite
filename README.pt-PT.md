# Revenue Intelligence Platform Suite

Template premium de plataforma analítica executiva para receita, retenção, governação de KPI e productização comercial.

Este ficheiro é a versão em Português (PT) do README principal em português do Brasil.

[![Platform](https://img.shields.io/badge/Platform-Revenue%20Intelligence-0F172A)](https://github.com/samuelmaia-analytics/revenue-intelligence-platform-suite)
[![App](https://img.shields.io/badge/Streamlit-Demo%20Publica-FF4B4B?logo=streamlit&logoColor=white)](https://revenue-intelligence-platform.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-CC_BY--NC_4.0-lightgrey.svg)](./LICENSE)

Demo pública: https://revenue-intelligence-platform.streamlit.app/

## Idioma
- English: [README.en.md](README.en.md)
- Português (BR): [README.pt-BR.md](README.pt-BR.md)
- Português (PT): [README.pt-PT.md](README.pt-PT.md)

## O Que Este Repositório É
Esta base já não é apenas uma montra técnica. Funciona agora como:
- plataforma analítica executiva
- template white-label para múltiplos clientes
- base para serviço recorrente
- fábrica de ativos comerciais, executivos e operacionais

Combina:
- apps executivas e operacionais
- contratos, observabilidade e quality gates
- semantic metric layer
- API executiva em FastAPI
- demo stack com Docker Compose
- review pack, proposal pack, microsite, deal room e GTM exports

## Para Quem É
- CRO, RevOps, liderança comercial
- Customer Success e retenção
- COO, CFO, estratégia e PMO executivo
- consultoras de analytics e data products
- empresas SaaS, healthtech, retalho e negócios recorrentes

## Resultados de Negócio
- priorizar risco e recuperação por impacto financeiro
- acelerar decisões executivas com KPI fiável
- transformar uma demo analítica numa solução comercial vendável
- reduzir o tempo de adaptação por cliente e por vertical

## Pacotes de Solução
- Revenue Command Center
- Retention Intelligence
- Executive KPI Governance
- Commercial Performance Analytics

Documentação:
- [docs/solutions/revenue-command-center.md](./docs/solutions/revenue-command-center.md)
- [docs/solutions/retention-intelligence.md](./docs/solutions/retention-intelligence.md)
- [docs/solutions/executive-kpi-governance.md](./docs/solutions/executive-kpi-governance.md)
- [docs/solutions/commercial-performance-analytics.md](./docs/solutions/commercial-performance-analytics.md)

## Arquitetura
```text
sources -> ingestion -> bronze -> silver -> gold -> semantic metrics -> executive insights -> apps -> action telemetry
```

Camadas principais:
- ingestão e conectores
- transformação e promoção de dados
- semantic layer e business metric layer
- modelação e recomendação
- observabilidade, scorecards e contratos
- serving executivo e comercial

Mais detalhe: [docs/architecture.md](./docs/architecture.md)

## Productização Comercial
Ativos gerados pela plataforma:
- `reports/showcase/summary.json`
- `reports/showcase/solution_profile.json`
- `reports/showcase/data_quality_scorecard.json`
- `reports/showcase/executive_insights.json`
- `dist/executive-review-pack/`
- `dist/client-proposal-pack/`
- `dist/client-microsite/`
- `dist/deal-rooms/<deal-slug>/`
- `dist/deal-rooms/<deal-slug>/sales-enablement/`

## Configuração Multi-Cliente
A configuração está externalizada em:
- `config/global.json`
- `config/environments/*.json`
- `config/clients/*.json`
- `config/solution_packages/*.json`
- `config/semantic_metrics.json`
- `config/proposal_defaults.json`

## Quickstart
Gerar artefactos do showcase:
```bash
python scripts/run_showcase_demo.py
```

Subir a app executiva:
```bash
streamlit run apps/executive-dashboard/app.py
```

Subir a API executiva:
```bash
uvicorn apps.executive_api.main:app --reload
```

Subir a stack local:
```bash
docker compose up --build
```

## Ativos Executivos e Comerciais
Executive review pack:
```bash
python scripts/build_executive_review_pack.py
```

Proposal pack:
```bash
python scripts/build_client_proposal_pack.py
```

Microsite por cliente:
```bash
python scripts/build_client_microsite.py
```

Deal room:
```bash
PROPOSAL_CLIENT_NAME="Acme Corp" DEAL_NAME="Acme Expansion FY26" python scripts/build_deal_room.py
```

Sales enablement bundle:
```bash
PROPOSAL_CLIENT_NAME="Acme Corp" DEAL_NAME="Acme Expansion FY26" python scripts/build_sales_enablement_bundle.py
```

GTM exports:
```bash
PROPOSAL_CLIENT_NAME="Acme Corp" DEAL_NAME="Acme Expansion FY26" python scripts/build_gtm_exports.py
```

## Documentação-Chave
- [docs/README.md](./docs/README.md)
- [docs/productization-roadmap.md](./docs/productization-roadmap.md)
- [docs/genai-governance.md](./docs/genai-governance.md)
- [docs/semantic-metric-layer.md](./docs/semantic-metric-layer.md)
- [docs/release-evidence-pack.md](./docs/release-evidence-pack.md)
- [docs/proposal-pack.md](./docs/proposal-pack.md)
- [docs/client-microsite.md](./docs/client-microsite.md)
- [docs/deal-room.md](./docs/deal-room.md)
- [docs/sales-enablement-bundle.md](./docs/sales-enablement-bundle.md)
- [docs/gtm-exports.md](./docs/gtm-exports.md)

## Como Isto Melhora o Posicionamento Comercial
O repositório demonstra agora:
- capacidade de plataforma
- clareza de produto
- governação de métricas
- experiência executiva
- readiness para venda consultiva e serviço recorrente

Para detalhe completo, use o README principal em português do Brasil: [README.md](README.md)

## License

This work is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0).

To view a copy of this license, visit:
https://creativecommons.org/licenses/by-nc/4.0/

[![License: CC BY-NC 4.0](https://licensebuttons.net/l/by-nc/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc/4.0/)

## Autor

**Samuel de Andrade Maia — Engenheiro de Dados Pleno | Analytics Engineer**

Atuo na **Avanade** desde **20/10/2026**, em Engenharia de Dados. Este é um **projeto pessoal de portfólio**; suas implementações, dados e resultados não representam entregas da Avanade ou de seus clientes.

[LinkedIn](https://www.linkedin.com/in/samuelmaia-analytics/) · [Portfólio](https://samuelmaia-analytics.github.io/samuelmaia-analytics/) · [Currículo em PDF](https://samuelmaia-analytics.github.io/samuelmaia-analytics/assets/Samuel_Maia_Curriculo.pdf)
