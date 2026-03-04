from pathlib import Path


def test_showcase_inputs_exist() -> None:
    root = Path(__file__).resolve().parents[1]
    required = [
        root / "apps" / "executive-dashboard" / "app.py",
        root / "scripts" / "run_showcase_demo.py",
        root
        / "modules"
        / "analise-vendas-python"
        / "dados_processados"
        / "vendas_simples.csv",
        root
        / "modules"
        / "revenue-intelligence"
        / "data"
        / "raw"
        / "E-commerce Customer Behavior - Sheet1.csv",
        root / "modules" / "revenue-intelligence" / "data" / "processed" / "metrics_report.json",
    ]
    for file_path in required:
        assert file_path.exists(), f"Missing required showcase input: {file_path}"
