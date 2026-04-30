from __future__ import annotations

import os
from dataclasses import dataclass, field, replace
from pathlib import Path


@dataclass(frozen=True)
class MetricDefinition:
    name: str
    description: str
    formula: str
    owner: str = "Revenue Analytics"


@dataclass(frozen=True)
class AppConfig:
    language_mode: str = "bilingual"
    currency_symbol: str = "$"


@dataclass(frozen=True)
class PipelineConfig:
    project_root: Path
    data_dir: Path
    raw_dir: Path
    bronze_dir: Path
    silver_dir: Path
    gold_dir: Path
    processed_dir: Path
    seed: int
    log_level: str
    logs_dir: Path = field(default_factory=lambda: Path("logs"))
    quality_report_name: str = "data_quality_report.json"
    app: AppConfig = field(default_factory=AppConfig)

    @classmethod
    def from_env(cls, project_root: Path | None = None) -> PipelineConfig:
        root = project_root or Path(__file__).resolve().parents[2]
        data_dir = Path(os.getenv("RIP_DATA_DIR", str(root / "data")))
        logs_dir = Path(os.getenv("RIP_LOG_DIR", str(root / "logs")))
        seed = int(os.getenv("RIP_SEED", "42"))
        log_level = os.getenv("RIP_LOG_LEVEL", "INFO").upper()
        language_mode = os.getenv("RIP_APP_LANG_MODE", "bilingual").strip().lower()
        if language_mode not in {"bilingual", "international"}:
            language_mode = "bilingual"
        currency_symbol = os.getenv("RIP_CURRENCY_SYMBOL", "$")

        return cls(
            project_root=root,
            data_dir=data_dir,
            raw_dir=data_dir / "raw",
            bronze_dir=data_dir / "bronze",
            silver_dir=data_dir / "silver",
            gold_dir=data_dir / "gold",
            processed_dir=data_dir / "processed",
            logs_dir=logs_dir,
            seed=seed,
            log_level=log_level,
            app=AppConfig(language_mode=language_mode, currency_symbol=currency_symbol),
        )

    def with_overrides(
        self,
        *,
        data_dir: Path | None = None,
        seed: int | None = None,
        log_level: str | None = None,
    ) -> PipelineConfig:
        if data_dir is None:
            return replace(
                self,
                seed=self.seed if seed is None else seed,
                log_level=self.log_level if log_level is None else log_level,
            )

        return replace(
            self,
            data_dir=data_dir,
            raw_dir=data_dir / "raw",
            bronze_dir=data_dir / "bronze",
            silver_dir=data_dir / "silver",
            gold_dir=data_dir / "gold",
            processed_dir=data_dir / "processed",
            seed=self.seed if seed is None else seed,
            log_level=self.log_level if log_level is None else log_level,
        )
