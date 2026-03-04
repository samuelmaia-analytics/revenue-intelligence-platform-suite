# Architecture

## Vision

A plataforma consolida analytics e ML de receita e retencao em um unico backbone de dados e servicos, com separacao clara por camadas.

## Logical Layers

- `platform/ingestion`: conectores e carga inicial de fontes operacionais.
- `platform/transform`: modelagem raw -> bronze -> silver -> gold.
- `platform/quality`: validacao de schemas e regras de negocio com Pandera.
- `platform/modeling`: treino e inferencia de churn, next purchase e LTV.
- `platform/orchestration`: fluxos Prefect para pipelines batch e retreinamento.
- `platform/serving`: contratos para batch scoring e API.

## Application Layer

- `apps/executive-dashboard`: visao executiva unica (receita, retencao, risco).
- `apps/sales-analytics`: exploracao operacional de vendas e KPI por canal.

## Monorepo Strategy

- Repos existentes entram em `modules/` via `git subtree`.
- Codigo comum vai para `packages/common`.
- Gradualmente, dependencias cruzadas dos modulos sao abstraidas para `platform/` e `packages/common`.

## Non-Functional Requirements

- Reprodutibilidade: pipelines versionados e rastreaveis.
- Confiabilidade: validacoes de qualidade antes de promover dados.
- Escalabilidade: separacao de computacao de transformacao e serving.
- Observabilidade: logs de fluxo e metricas de qualidade/modelo.
