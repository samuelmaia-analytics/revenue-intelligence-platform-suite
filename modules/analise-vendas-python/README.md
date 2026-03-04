> This repository is part of the **Revenue-Intelligence-Platform-Suite**
> Main platform: ../../README.md

## Language
- English: [README.en.md](README.en.md)
- Portugues (BR): [README.md](README.md)
- Portugues (PT): [README.pt-PT.md](README.pt-PT.md)

# 📊 Sales Analytics Dashboard – End-to-End Data Project

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-green)
![NumPy](https://img.shields.io/badge/NumPy-Numerical%20Computing-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-Interactive%20Dashboard-red)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-purple)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![Pytest](https://img.shields.io/badge/Tests-Pytest-yellow)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

🚀 **Deploy:**  
https://analys-vendas-python.streamlit.app/

📂 **Repositório:**  
https://github.com/samuelmaiapro/analise-vendas-python

---

## Summary
- Executive Summary
- Data Source
- Tech Stack
- How to Run
- Where it fits in the platform

## Executive Summary

Projeto **end-to-end de Sales Analytics**, estruturado como um caso real de negócio.

O sistema transforma dados transacionais em decisões estratégicas por meio de:

- 📈 Análise de crescimento periódico  
- 🧾 Métricas executivas consolidadas  
- 🧩 Análise de concentração (Pareto automático)  
- 📅 Comparação Year-over-Year (YoY)  
- 📊 Visualizações interativas  

---

# 📊 Fonte de Dados

## 1️⃣ Upload Dinâmico de CSV
- Seleção automática de coluna de data  
- Seleção automática de coluna de valor  
- Compatível com qualquer dataset transacional  

## 2️⃣ Dataset Base Utilizado

Kaggle – Sample Sales Data  
https://www.kaggle.com/datasets/kyanyoga/sample-sales-data  

Principais resultados identificados:

- Receita total analisada: **$10M+**
- Crescimento médio mensal: **~14%**
- Top 3 linhas de produto representam **~70% da receita**
- Pico sazonal identificado em **novembro**

## 3️⃣ Dados Simulados

Fallback automático com:
- Tendência de crescimento  
- Sazonalidade anual  
- Ruído estatístico controlado  

---

# 🧾 Métricas Executivas

- Receita Total  
- Pico Sazonal (detecção automática)  
- Concentração Top 3 por dimensão  
- Crescimento Médio  
- Melhor e Pior Período  
- YoY (Year-over-Year) mensal  

---

# 🧩 Pareto Automático

O sistema gera automaticamente:

- Ranking por dimensão (produto, categoria, país, etc.)
- Percentual individual de participação
- Percentual acumulado
- Visualização combinada (barras + linha acumulada)

Permite identificar concentração de receita e risco de dependência.

---

# 📅 Comparação YoY

Cálculo automático de:

- Total mensal agregado
- Variação absoluta YoY
- Variação percentual YoY
- Visualização com eixo duplo (Total + % YoY)

Permite avaliar crescimento sustentável e sazonalidade estrutural.

---

# 🔄 Pipeline de Dados

```mermaid
flowchart LR
    A[Ingestão CSV] --> B[Tratamento & Tipagem]
    B --> C[Agregações Temporais]
    C --> D[KPIs Executivos]
    D --> E[Pareto]
    D --> F[YoY]
    E --> G[Visualização Interativa]
    F --> G
    G --> H[Deploy Streamlit]
```
# 🏗 Arquitetura

Estruturado com foco em separação de responsabilidades:

Funções utilitárias isoladas

Cálculos desacoplados

Funções dedicadas para Pareto e YoY

Cache inteligente (@st.cache_data)

Tratamento seguro de tipos (datetime / numeric)

Fallback robusto de dados

# 🎯 Executive Business Case
# 🔴 Risco Identificado

Alta concentração de receita (~70%) em poucas linhas de produto.

# 🟢 Oportunidade

Crescimento médio mensal consistente (~14%).

# 🟡 Estratégia Recomendada

Diversificação de portfólio

Planejamento antecipado para pico sazonal (Q4)

Padronização e governança de KPIs

# 🛠 Stack Tecnológica

Python

Pandas

NumPy

Plotly

Streamlit

Docker

Pytest

▶ Execução
Local
```
streamlit run app.py
```
Docker
```
docker-compose up --build
```
# 🚀 Roadmap

Integração com banco de dados

Pipeline ETL automatizado

Monitoramento de performance

Deploy escalável em cloud

Camada semântica de métricas

# 🧠 Diferencial Estratégico

Este projeto demonstra:

Capacidade técnica end-to-end

Tradução de dados em decisões executivas

Arquitetura preparada para evolução

Maturidade analítica e visão estratégica

⭐ Se este projeto foi útil ou inspirador, considere deixar uma estrela.

## Where it fits in the platform
- Layer: App + Analytics
- Inputs: Transactional sales data, product and channel dimensions
- Outputs: Interactive sales dashboards, business KPIs, actionable analysis for leadership









