# Ingestion

## Purpose
This namespace represents the source-system entry point of the platform.

## Scope
- connectors for CRM, billing, ERP, commerce, and flat-file ingestion
- ingestion-safe normalization before downstream modeling
- compatibility patterns for multi-client connector substitution

## Architectural Role
`platform/ingestion/` exists to make source integration explicit in the platform blueprint, even when a given client implementation still relies on module-local loaders or demo data.
