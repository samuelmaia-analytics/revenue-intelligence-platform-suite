# Documentacao Do Churn Prediction

## Proposito
Este conjunto de documentos apoia o modulo `churn-prediction` com navegacao por idioma e contexto de implementacao.

## Pontos Principais
- README do modulo: [../README.md](../README.md)
- English: [README.en.md](README.en.md)
- Portugues (PT): [README.pt-PT.md](README.pt-PT.md)

## Sobre O Modulo
`churn-prediction` e o componente de modelagem de risco de churn da plataforma. Ele existe para identificar exposicao de cancelamento, apoiar a priorizacao de retencao e fornecer sinais modelados para fluxos executivos de revisao.

## Arquitetura Em Alto Nivel
```mermaid
flowchart LR
  A[Dados Brutos De Clientes] --> B[Preparacao]
  B --> C[Engenharia De Features]
  C --> D[Modelagem]
  D --> E[Scores De Risco]
  E --> F[Dashboard E Artefatos Da Plataforma]
```

## Ordem Recomendada De Leitura
1. Ler [../README.md](../README.md) para o posicionamento do modulo.
2. Revisar contratos, reports e scripts na raiz do modulo.
3. Conectar o modulo a suite principal em [../../../README.md](../../../README.md).
