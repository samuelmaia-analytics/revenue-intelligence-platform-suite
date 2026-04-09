# Modules

## Purpose
This directory consolidates the flagship domain repositories that power the platform narrative, demo flows, and reusable client solution paths.

The goal is not only code aggregation. `modules/` acts as the portfolio layer that proves the suite can combine multiple analytical products into one executive operating system.

## What Lives Here
- `modules/revenue-intelligence`
- `modules/churn-prediction`
- `modules/amazon-sales-analysis`
- `modules/analise-vendas-python`
- `modules/data-senior-analytics`

## How These Modules Are Used
- as integrated data and business logic sources for the executive showcase
- as proof of depth across revenue, churn, sales, and decision analytics
- as reusable accelerators for client-specific solution packaging
- as portfolio evidence for architecture, modeling, and delivery maturity

## Repository Convention
Modules are imported and maintained with `git subtree` to preserve independent history while keeping the monorepo operationally cohesive.

Example:
```bash
git remote add <alias> <repo-url>
git subtree add --prefix modules/<module-name> <alias> main --squash
```

## Positioning
The suite-level README explains the commercial and executive framing. Each module README keeps its own domain identity, but `modules/` is the place where they become part of one sellable platform story.
