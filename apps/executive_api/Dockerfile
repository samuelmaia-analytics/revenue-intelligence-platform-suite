FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md requirements.txt ./
COPY apps ./apps
COPY packages ./packages
COPY config ./config
COPY reports ./reports
COPY platform_connectors ./platform_connectors
COPY platform_observability ./platform_observability

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -e .

EXPOSE 8000

CMD ["uvicorn", "apps.executive_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
