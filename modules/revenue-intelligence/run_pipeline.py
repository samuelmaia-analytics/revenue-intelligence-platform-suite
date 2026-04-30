from pathlib import Path

from src.config import PipelineConfig
from src.orchestration.pipeline import run_pipeline

if __name__ == "__main__":
    run_pipeline(PipelineConfig.from_env(Path(__file__).resolve().parent))
