# Common Package

## Purpose
`packages/common/` contains the shared productization layer for the whole suite. This is where reusable platform behaviors live instead of being duplicated across apps, scripts, and module integrations.

## Main Responsibilities
- configuration loading and layer merging
- semantic metric catalog access
- executive artifact generation
- contract validation support
- tenant-secret readiness checks
- approval workflow generation
- SSO identity resolution

## Key Components
- `configuration.py`: global, environment, client, and solution-package configuration
- `executive.py`: solution profile, scorecard, recommended actions, and executive insights
- `semantic_metrics.py`: business metric catalog access
- `secrets.py`: masked tenant secret status and template-driven readiness
- `approvals.py`: formal sign-off workflow for deal rooms and delivery readiness
- `sso.py`: trusted-header SSO enforcement helpers
- `contracts/`: versioned schemas and validation utilities

## Why It Matters
This directory is one of the main reasons the repository behaves like a reusable client platform instead of a collection of demos. It centralizes the logic that makes white-label adaptation, governance, and executive outputs consistent.
