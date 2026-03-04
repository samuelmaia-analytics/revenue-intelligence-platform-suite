# Modules

Diretorio reservado para importacao dos repos existentes via `git subtree`.

## Planned module paths

- `modules/revenue-intelligence`
- `modules/churn-prediction`
- `modules/amazon-sales-analysis`
- `modules/analise-vendas-python`
- `modules/data-senior-analytics`

## Import command template

```bash
git remote add <alias> <repo-url>
git subtree add --prefix modules/<module-name> <alias> main --squash
```
