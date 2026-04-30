from __future__ import annotations

import shutil

from src.analytics.recommendations import build_recommendations
from src.analytics.reporting import (
    build_business_outcomes,
    build_executive_report,
    build_executive_summary,
)
from src.analytics.semantic_layer import (
    calculate_cac,
    calculate_ltv,
    cohort_analysis,
    rfm_segmentation,
    unit_economics,
)
from src.core.config import PipelineConfig
from src.core.logging import configure_logging, get_logger
from src.ingestion.raw import build_bronze_layer, save_raw_datasets
from src.models.training import train_and_score_models
from src.transform.features import build_customer_features
from src.transform.silver import build_silver_layer
from src.warehouse import build_star_schema
from src.warehouse_loader import WarehouseConfig, load_gold_to_warehouse

LOGGER = get_logger("revenue_intelligence.pipeline")


def _log_stage(stage: str, message: str, **extra: object) -> None:
    LOGGER.info(message, extra={"stage": stage, "status": "success", **extra})


def run_pipeline(cfg: PipelineConfig) -> None:
    configure_logging(cfg.log_level, cfg.logs_dir)
    cfg.processed_dir.mkdir(parents=True, exist_ok=True)
    warehouse_config = WarehouseConfig.from_env()

    _log_stage("pipeline", "Pipeline started.", artifact=str(cfg.data_dir))
    customers_path, orders_path, marketing_path = save_raw_datasets(cfg.raw_dir, seed=cfg.seed)
    bronze_customers, bronze_orders, bronze_marketing = build_bronze_layer(
        customers_path, orders_path, marketing_path, cfg.bronze_dir
    )
    silver_customers, silver_orders, silver_marketing = build_silver_layer(
        bronze_customers,
        bronze_orders,
        bronze_marketing,
        cfg.silver_dir,
        quality_report_path=cfg.processed_dir / cfg.quality_report_name,
    )

    features_df = build_customer_features(silver_customers, silver_orders, cfg.processed_dir)
    build_star_schema(silver_customers, silver_orders, cfg.gold_dir)
    _log_stage("warehouse", "Gold star schema generated.", artifact=str(cfg.gold_dir))

    for table in ["dim_customers.csv", "dim_date.csv", "dim_channel.csv", "fact_orders.csv"]:
        shutil.copy2(cfg.gold_dir / table, cfg.processed_dir / table)

    churn_results, next_purchase_results, scored_df = train_and_score_models(
        features_df, cfg.processed_dir
    )
    _log_stage("modeling", "Scoring completed.", rows=len(scored_df))

    ltv_df = calculate_ltv(scored_df)
    cac_df = calculate_cac(silver_marketing, silver_customers)
    rfm_df = rfm_segmentation(silver_orders, silver_customers)
    cohort_df = cohort_analysis(silver_orders, silver_customers)
    unit_df = unit_economics(ltv_df, cac_df)
    rec_df = build_recommendations(ltv_df, cac_df)

    ltv_df.to_csv(cfg.processed_dir / "ltv.csv", index=False)
    cac_df.to_csv(cfg.processed_dir / "cac_by_channel.csv", index=False)
    rfm_df.to_csv(cfg.processed_dir / "rfm_segments.csv", index=False)
    cohort_df.to_csv(cfg.processed_dir / "cohort_retention.csv", index=False)
    unit_df.to_csv(cfg.processed_dir / "unit_economics.csv", index=False)
    rec_df.to_csv(cfg.processed_dir / "recommendations.csv", index=False)
    build_executive_report(
        recommendations_df=rec_df,
        churn_results=churn_results,
        next_purchase_results=next_purchase_results,
        output_path=cfg.processed_dir / "executive_report.json",
    )
    build_executive_summary(
        recommendations_df=rec_df,
        scored_df=scored_df,
        unit_economics_df=unit_df,
        output_path=cfg.processed_dir / "executive_summary.json",
    )
    build_business_outcomes(
        recommendations_df=rec_df,
        unit_economics_df=unit_df,
        outcomes_path=cfg.processed_dir / "business_outcomes.json",
        top_actions_path=cfg.processed_dir / "top_10_actions.csv",
    )
    _log_stage("analytics", "Semantic layer and reporting outputs published.", rows=len(rec_df))

    load_gold_to_warehouse(cfg.gold_dir, warehouse_config)
    LOGGER.info(
        "Pipeline completed successfully.",
        extra={"stage": "pipeline", "provider": warehouse_config.provider, "status": "success"},
    )
