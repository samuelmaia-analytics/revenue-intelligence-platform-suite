PYTHON ?= python
CLIENT_PROFILE ?= saas_b2b
SOLUTION_PACKAGE ?= revenue_command_center
DEPLOYMENT_ENV ?= showcase
PROPOSAL_CLIENT_NAME ?= Flagship Client
DEAL_NAME ?= Flagship Client
RELEASE_TAG ?= local
PUBLISH_TARGET ?= static_bundle
PUBLISH_BASE_URL ?= https://demo.example.com

.PHONY: install lint test validate showcase app api demo-stack protected-demo-stack google-workspace-demo-stack review-pack proposal-pack microsite deal-room approval-pack publish-bundle prepare-pages sales-bundle gtm-exports evidence-pack industry-packs benchmark tenant-secrets-check docs-index

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e ".[dev]"

lint:
	ruff check apps scripts packages/common tests README.md README.pt-BR.md README.pt-PT.md docs .github/workflows

test:
	pytest -q

validate:
	$(PYTHON) scripts/validate_showcase_artifacts.py

tenant-secrets-check:
	CLIENT_PROFILE=$(CLIENT_PROFILE) DEPLOYMENT_ENV=$(DEPLOYMENT_ENV) $(PYTHON) scripts/check_tenant_secrets.py

showcase:
	CLIENT_PROFILE=$(CLIENT_PROFILE) SOLUTION_PACKAGE=$(SOLUTION_PACKAGE) DEPLOYMENT_ENV=$(DEPLOYMENT_ENV) $(PYTHON) scripts/run_showcase_demo.py

app:
	streamlit run apps/executive-dashboard/app.py

api:
	uvicorn apps.executive_api.main:app --reload

demo-stack:
	docker compose up --build

protected-demo-stack:
	PLATFORM_SSO_MODE=trusted_header docker compose --profile protected up --build

google-workspace-demo-stack:
	PLATFORM_SSO_MODE=trusted_header OAUTH2_PROXY_PROVIDER=google docker compose --profile protected --env-file deploy/oauth2-proxy/google-workspace.env.example up --build

review-pack:
	$(PYTHON) scripts/build_executive_review_pack.py

proposal-pack:
	PROPOSAL_CLIENT_NAME="$(PROPOSAL_CLIENT_NAME)" $(PYTHON) scripts/build_client_proposal_pack.py

microsite:
	PROPOSAL_CLIENT_NAME="$(PROPOSAL_CLIENT_NAME)" $(PYTHON) scripts/build_client_microsite.py

deal-room:
	PROPOSAL_CLIENT_NAME="$(PROPOSAL_CLIENT_NAME)" DEAL_NAME="$(DEAL_NAME)" RELEASE_TAG="$(RELEASE_TAG)" $(PYTHON) scripts/build_deal_room.py

approval-pack:
	PROPOSAL_CLIENT_NAME="$(PROPOSAL_CLIENT_NAME)" DEAL_NAME="$(DEAL_NAME)" RELEASE_TAG="$(RELEASE_TAG)" $(PYTHON) scripts/build_formal_approval_pack.py

publish-bundle:
	PROPOSAL_CLIENT_NAME="$(PROPOSAL_CLIENT_NAME)" DEAL_NAME="$(DEAL_NAME)" PUBLISH_TARGET="$(PUBLISH_TARGET)" PUBLISH_BASE_URL="$(PUBLISH_BASE_URL)" $(PYTHON) scripts/build_external_publication_bundle.py

prepare-pages:
	PROPOSAL_CLIENT_NAME="$(PROPOSAL_CLIENT_NAME)" DEAL_NAME="$(DEAL_NAME)" PUBLISH_BASE_URL="$(PUBLISH_BASE_URL)" $(PYTHON) scripts/prepare_github_pages_publication.py

sales-bundle:
	PROPOSAL_CLIENT_NAME="$(PROPOSAL_CLIENT_NAME)" DEAL_NAME="$(DEAL_NAME)" $(PYTHON) scripts/build_sales_enablement_bundle.py

gtm-exports:
	PROPOSAL_CLIENT_NAME="$(PROPOSAL_CLIENT_NAME)" DEAL_NAME="$(DEAL_NAME)" $(PYTHON) scripts/build_gtm_exports.py

evidence-pack:
	RELEASE_TAG="$(RELEASE_TAG)" $(PYTHON) scripts/build_release_evidence_pack.py

industry-packs:
	$(PYTHON) scripts/build_industry_demo_packs.py

benchmark:
	$(PYTHON) scripts/build_synthetic_benchmark.py

docs-index:
	$(PYTHON) -c "from pathlib import Path; print((Path('docs') / 'README.md').read_text(encoding='utf-8'))"
