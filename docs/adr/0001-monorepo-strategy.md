# ADR 0001: Monorepo Strategy with Git Subtree

- Status: Accepted
- Date: 2026-03-04

## Context

Os ativos de dados e ML estao divididos em repositorios com maturidades diferentes. O objetivo e operar como plataforma unica sem perder historico.

## Decision

Adotar monorepo com importacao dos repos existentes via `git subtree` sob `modules/`.

## Consequences

- Positivas:
  - Clone unico e onboarding simples.
  - Governanca central de padroes (lint, tests, CI, docs).
  - Narrativa clara de plataforma no portfolio.
- Negativas:
  - Sincronizacao com upstream exige disciplina.
  - Historico pode ficar mais denso com atualizacoes de subtree.

## Follow-up

- Criar playbook de update de subtree.
- Definir ownership por modulo e contratos de interface.
