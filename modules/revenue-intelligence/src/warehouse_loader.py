from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import pandas as pd

LOGGER = logging.getLogger("revenue_intelligence.warehouse_loader")

WarehouseProvider = Literal["none", "bigquery", "snowflake"]


@dataclass(frozen=True)
class WarehouseConfig:
    provider: WarehouseProvider
    dataset: str
    schema: str
    bq_project: str | None = None
    bq_location: str = "US"
    sf_account: str | None = None
    sf_user: str | None = None
    sf_password: str | None = None
    sf_warehouse: str | None = None
    sf_database: str | None = None
    sf_role: str | None = None

    @classmethod
    def from_env(cls) -> WarehouseConfig:
        provider = os.getenv("RIP_WAREHOUSE_PROVIDER", "none").strip().lower()
        if provider not in {"none", "bigquery", "snowflake"}:
            raise ValueError(
                "Invalid RIP_WAREHOUSE_PROVIDER. Use one of: none, bigquery, snowflake."
            )

        return cls(
            provider=provider,  # type: ignore[arg-type]
            dataset=os.getenv("RIP_WAREHOUSE_DATASET", "revenue_intelligence"),
            schema=os.getenv("RIP_WAREHOUSE_SCHEMA", "analytics"),
            bq_project=os.getenv("RIP_BQ_PROJECT"),
            bq_location=os.getenv("RIP_BQ_LOCATION", "US"),
            sf_account=os.getenv("RIP_SF_ACCOUNT"),
            sf_user=os.getenv("RIP_SF_USER"),
            sf_password=os.getenv("RIP_SF_PASSWORD"),
            sf_warehouse=os.getenv("RIP_SF_WAREHOUSE"),
            sf_database=os.getenv("RIP_SF_DATABASE"),
            sf_role=os.getenv("RIP_SF_ROLE"),
        )


def load_gold_to_warehouse(gold_dir: Path, config: WarehouseConfig) -> None:
    if config.provider == "none":
        LOGGER.info("Warehouse load skipped (RIP_WAREHOUSE_PROVIDER=none).")
        return

    tables = {
        "dim_customers": gold_dir / "dim_customers.csv",
        "dim_date": gold_dir / "dim_date.csv",
        "dim_channel": gold_dir / "dim_channel.csv",
        "fact_orders": gold_dir / "fact_orders.csv",
    }
    missing = [str(path) for path in tables.values() if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Gold tables not found for warehouse load: {missing}")

    if config.provider == "bigquery":
        _load_to_bigquery(tables, config)
        return

    if config.provider == "snowflake":
        _load_to_snowflake(tables, config)
        return

    raise ValueError(f"Unsupported warehouse provider: {config.provider}")


def _load_to_bigquery(tables: dict[str, Path], config: WarehouseConfig) -> None:
    if not config.bq_project:
        raise ValueError("RIP_BQ_PROJECT is required when RIP_WAREHOUSE_PROVIDER=bigquery.")

    try:
        from google.cloud import bigquery
    except ImportError as exc:
        raise ImportError(
            "google-cloud-bigquery is required for BigQuery loads. "
            "Install dependencies from requirements-warehouse.txt."
        ) from exc

    client = bigquery.Client(project=config.bq_project, location=config.bq_location)
    dataset_id = f"{config.bq_project}.{config.dataset}"
    client.create_dataset(bigquery.Dataset(dataset_id), exists_ok=True)

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    for table_name, csv_path in tables.items():
        destination = f"{dataset_id}.{table_name}"
        with csv_path.open("rb") as file_obj:
            load_job = client.load_table_from_file(file_obj, destination, job_config=job_config)
            load_job.result()
        LOGGER.info("Loaded %s into BigQuery table %s", csv_path.name, destination)


def _load_to_snowflake(tables: dict[str, Path], config: WarehouseConfig) -> None:
    required_values = {
        "RIP_SF_ACCOUNT": config.sf_account,
        "RIP_SF_USER": config.sf_user,
        "RIP_SF_PASSWORD": config.sf_password,
        "RIP_SF_WAREHOUSE": config.sf_warehouse,
        "RIP_SF_DATABASE": config.sf_database,
    }
    missing = [key for key, value in required_values.items() if not value]
    if missing:
        missing_str = ", ".join(missing)
        raise ValueError(
            f"Missing required Snowflake variables for warehouse load: {missing_str}."
        )

    try:
        import snowflake.connector
        from snowflake.connector.pandas_tools import write_pandas
    except ImportError as exc:
        raise ImportError(
            "snowflake-connector-python is required for Snowflake loads. "
            "Install dependencies from requirements-warehouse.txt."
        ) from exc

    connection = snowflake.connector.connect(
        account=config.sf_account,
        user=config.sf_user,
        password=config.sf_password,
        warehouse=config.sf_warehouse,
        database=config.sf_database,
        schema=config.schema,
        role=config.sf_role,
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {config.schema}")

        for table_name, csv_path in tables.items():
            dataframe = pd.read_csv(csv_path)
            success, _, rows_loaded, _ = write_pandas(
                conn=connection,
                df=dataframe,
                table_name=table_name.upper(),
                schema=config.schema,
                auto_create_table=True,
                overwrite=True,
            )
            if not success:
                raise RuntimeError(f"Snowflake load failed for table {table_name}.")
            LOGGER.info(
                "Loaded %s into Snowflake table %s.%s (%s rows)",
                csv_path.name,
                config.schema,
                table_name.upper(),
                rows_loaded,
            )
    finally:
        connection.close()
