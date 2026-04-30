from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

import pandas as pd


class DataQualityError(ValueError):
    pass


@dataclass(frozen=True)
class DataValidationRule:
    required_columns: tuple[str, ...]
    unique_columns: tuple[str, ...] = ()
    non_null_columns: tuple[str, ...] = ()


@dataclass
class DataQualityReport:
    table_name: str
    status: str
    row_count: int
    missing_columns: list[str] = field(default_factory=list)
    null_counts: dict[str, int] = field(default_factory=dict)
    duplicate_count: int = 0
    consistency_issues: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def validate_dataset(
    df: pd.DataFrame,
    *,
    table_name: str,
    rule: DataValidationRule,
    consistency_checks: list[tuple[bool, str]] | None = None,
) -> DataQualityReport:
    missing = sorted(set(rule.required_columns).difference(df.columns))
    null_counts = {
        col: int(df[col].isna().sum())
        for col in rule.non_null_columns
        if col in df.columns and int(df[col].isna().sum()) > 0
    }
    duplicate_count = 0
    if rule.unique_columns and set(rule.unique_columns).issubset(df.columns):
        duplicate_count = int(df.duplicated(subset=list(rule.unique_columns)).sum())

    consistency_issues = [
        message for passed, message in (consistency_checks or []) if not bool(passed)
    ]
    status = (
        "failed"
        if missing or null_counts or duplicate_count > 0 or consistency_issues
        else "passed"
    )

    return DataQualityReport(
        table_name=table_name,
        status=status,
        row_count=int(len(df)),
        missing_columns=missing,
        null_counts=null_counts,
        duplicate_count=duplicate_count,
        consistency_issues=consistency_issues,
    )


def _raise_for_failed_reports(reports: list[DataQualityReport]) -> None:
    failed = [report for report in reports if report.status != "passed"]
    if not failed:
        return
    message = "; ".join(
        [
            f"{report.table_name}: missing={report.missing_columns}, "
            f"nulls={report.null_counts}, duplicates={report.duplicate_count}, "
            f"consistency={report.consistency_issues}"
            for report in failed
        ]
    )
    raise DataQualityError(f"Data quality validation failed. {message}")


def validate_silver_tables(
    customers: pd.DataFrame,
    orders: pd.DataFrame,
    marketing: pd.DataFrame,
    *,
    report_path: Path | None = None,
) -> list[DataQualityReport]:
    reports = [
        validate_dataset(
            customers,
            table_name="silver_customers",
            rule=DataValidationRule(
                required_columns=("customer_id", "signup_date", "channel", "segment"),
                unique_columns=("customer_id",),
                non_null_columns=("customer_id", "signup_date", "channel", "segment"),
            ),
        ),
        validate_dataset(
            orders,
            table_name="silver_orders",
            rule=DataValidationRule(
                required_columns=("order_id", "customer_id", "order_date", "order_value"),
                unique_columns=("order_id",),
                non_null_columns=("order_id", "customer_id", "order_date", "order_value"),
            ),
            consistency_checks=[
                ((orders["order_value"] > 0).all(), "order_value must be positive"),
                (
                    orders["customer_id"].isin(customers["customer_id"]).all(),
                    "orders contain unknown customer_id",
                ),
            ],
        ),
        validate_dataset(
            marketing,
            table_name="silver_marketing_spend",
            rule=DataValidationRule(
                required_columns=("channel", "marketing_spend"),
                unique_columns=("channel",),
                non_null_columns=("channel", "marketing_spend"),
            ),
            consistency_checks=[
                ((marketing["marketing_spend"] >= 0).all(), "marketing_spend must be non-negative")
            ],
        ),
    ]

    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            json.dumps([report.to_dict() for report in reports], indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    _raise_for_failed_reports(reports)
    return reports
