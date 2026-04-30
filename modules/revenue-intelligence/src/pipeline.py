import argparse
from pathlib import Path

from src.config import PipelineConfig
from src.orchestration.pipeline import run_pipeline


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Revenue Intelligence Platform CLI")
    subparsers = parser.add_subparsers(dest="command")

    run_cmd = subparsers.add_parser("run", help="Run end-to-end pipeline")
    run_cmd.add_argument("--data-dir", type=str, default=None, help="Override data directory.")
    run_cmd.add_argument("--seed", type=int, default=None, help="Override random seed.")
    run_cmd.add_argument(
        "--log-level",
        type=str,
        default=None,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Override log level.",
    )
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command != "run":
        parser.print_help()
        return

    cfg = PipelineConfig.from_env(Path(__file__).resolve().parents[1])
    cfg = cfg.with_overrides(
        data_dir=Path(args.data_dir) if args.data_dir else None,
        seed=args.seed,
        log_level=args.log_level,
    )
    run_pipeline(cfg)


if __name__ == "__main__":
    main()
