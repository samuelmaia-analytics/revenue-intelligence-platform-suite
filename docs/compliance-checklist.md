# Compliance Checklist (LGPD/GDPR Baseline)

## Purpose

Provide a practical baseline for data governance in analytics and ML workflows.

## Data Governance Controls

- [ ] Data source registered with owner and legal basis.
- [ ] Data minimization applied (only required fields).
- [ ] Retention policy documented for each dataset.
- [ ] Access control defined for sensitive data paths.
- [ ] Data contracts include sensitive-field rules where needed.

## Privacy Controls

- [ ] PII removed or anonymized before repository usage.
- [ ] Pseudonymization strategy documented for identifiers.
- [ ] Re-identification risk reviewed before sharing outputs.
- [ ] Consent requirements reviewed with business/legal stakeholders.

## Model and Analytics Controls

- [ ] Feature list reviewed for sensitive proxies.
- [ ] Segment-level bias checks documented.
- [ ] Explainability output available for executive decisions.
- [ ] Drift monitoring and retraining policy defined.

## Auditability

- [ ] Versioned pipelines and model artifacts tracked.
- [ ] KPI scorecard updates logged with date and owner.
- [ ] Incident and remediation notes recorded for data/ML failures.

## Review Cadence

- Weekly: pipeline health and contract pass rates.
- Monthly: KPI, privacy, and retention policy checks.
- Quarterly: full compliance review and control updates.
