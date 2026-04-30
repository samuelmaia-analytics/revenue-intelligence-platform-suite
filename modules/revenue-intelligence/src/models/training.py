from __future__ import annotations

import json
import pickle
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

try:
    from sklearn.compose import ColumnTransformer
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import precision_recall_curve, roc_auc_score, roc_curve
    from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler

    SKLEARN_AVAILABLE = True
except ModuleNotFoundError:  # pragma: no cover - optional dependency in lightweight envs
    ColumnTransformer = Any  # type: ignore[assignment]
    Pipeline = Any  # type: ignore[assignment]
    RandomForestClassifier = LogisticRegression = OneHotEncoder = StandardScaler = None
    precision_recall_curve = roc_auc_score = roc_curve = None
    StratifiedKFold = cross_val_score = train_test_split = None
    SKLEARN_AVAILABLE = False

try:
    import joblib
except ModuleNotFoundError:  # pragma: no cover
    joblib = None


def _build_preprocessor() -> tuple[ColumnTransformer, list[str], list[str]]:
    numeric_features = [
        "recency_days",
        "frequency",
        "monetary",
        "avg_order_value",
        "tenure_days",
        "arpu",
    ]
    categorical_features = ["channel", "segment"]
    if not SKLEARN_AVAILABLE:
        return None, numeric_features, categorical_features
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ]
    )
    return preprocessor, numeric_features, categorical_features


def _safe_roc_auc(y_true: pd.Series, y_prob: np.ndarray) -> float:
    if roc_auc_score is None:
        return float("nan")
    if y_true.nunique() < 2:
        return float("nan")
    return float(roc_auc_score(y_true, y_prob))


def _temporal_split_indices(
    df: pd.DataFrame, split_ratio: float = 0.8
) -> tuple[pd.Index, pd.Index]:
    ordered_idx = df.sort_values("signup_date").index
    split_at = int(len(ordered_idx) * split_ratio)
    split_at = max(1, min(split_at, len(ordered_idx) - 1))
    return ordered_idx[:split_at], ordered_idx[split_at:]


def _build_evaluation_split(df: pd.DataFrame, y: pd.Series) -> tuple[pd.Index, pd.Index, str]:
    train_idx, test_idx = _temporal_split_indices(df)
    y_train, y_test = y.loc[train_idx], y.loc[test_idx]
    if y_train.nunique() > 1 and y_test.nunique() > 1:
        return train_idx, test_idx, "temporal"

    if y.nunique() < 2 or train_test_split is None:
        return train_idx, test_idx, "temporal_single_class"

    train_idx, test_idx = train_test_split(y.index, test_size=0.2, random_state=42, stratify=y)
    return pd.Index(train_idx), pd.Index(test_idx), "stratified_fallback"


def _evaluate_pipeline_temporal(
    pipeline: Pipeline, x: pd.DataFrame, y: pd.Series, ordered_df: pd.DataFrame
) -> dict:
    train_idx, test_idx, split_strategy = _build_evaluation_split(ordered_df, y)
    x_train, x_test = x.loc[train_idx], x.loc[test_idx]
    y_train, y_test = y.loc[train_idx], y.loc[test_idx]

    class_count = y_train.value_counts()
    min_class_count = int(class_count.min()) if not class_count.empty else 0
    n_splits = min(5, min_class_count)
    if n_splits >= 2 and y_train.nunique() > 1:
        cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
        cv_scores = cross_val_score(pipeline, x_train, y_train, cv=cv, scoring="roc_auc")
        cv_mean = float(np.mean(cv_scores))
        cv_std = float(np.std(cv_scores))
    else:
        cv_mean = float("nan")
        cv_std = float("nan")

    pipeline.fit(x_train, y_train)
    y_prob = pipeline.predict_proba(x_test)[:, 1]
    roc_auc = _safe_roc_auc(y_test, y_prob)
    if y_test.nunique() > 1:
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        precision, recall, _ = precision_recall_curve(y_test, y_prob)
        fpr_list, tpr_list = fpr.tolist(), tpr.tolist()
        precision_list, recall_list = precision.tolist(), recall.tolist()
    else:
        fpr_list, tpr_list, precision_list, recall_list = [], [], [], []

    return {
        "model": pipeline,
        "cv_roc_auc_mean": cv_mean,
        "cv_roc_auc_std": cv_std,
        "temporal_test_roc_auc": roc_auc,
        "split_strategy": split_strategy,
        "train_size": int(len(x_train)),
        "test_size": int(len(x_test)),
        "fpr": fpr_list,
        "tpr": tpr_list,
        "precision": precision_list,
        "recall": recall_list,
        "x_test_index": x_test.index.tolist(),
        "y_prob_test": y_prob.tolist(),
    }


def _persist_model(model: Pipeline, path: Path) -> None:
    if joblib is not None:
        joblib.dump(model, path)
        return
    with path.open("wb") as model_file:
        pickle.dump(model, model_file)


def _heuristic_probability(
    df: pd.DataFrame,
    *,
    positive_columns: list[str],
    negative_columns: list[str],
) -> np.ndarray:
    working = pd.DataFrame(index=df.index)
    for column in positive_columns + negative_columns:
        working[column] = pd.to_numeric(df[column], errors="coerce").fillna(0.0)

    score = pd.Series(0.0, index=df.index, dtype=float)
    for column in positive_columns:
        score = score.add(working[column].rank(pct=True), fill_value=0.0)
    for column in negative_columns:
        score = score.sub(working[column].rank(pct=True), fill_value=0.0)

    centered = score - float(score.mean())
    probability = 1.0 / (1.0 + np.exp(-centered.to_numpy(dtype=float)))
    return probability.clip(0.01, 0.99)


def _heuristic_model_summary(
    ordered_df: pd.DataFrame,
    y: pd.Series,
    *,
    target_name: str,
    positive_columns: list[str],
    negative_columns: list[str],
) -> tuple[dict[str, Any], np.ndarray]:
    train_idx, test_idx, split_strategy = _build_evaluation_split(ordered_df, y)
    y_train, y_test = y.loc[train_idx], y.loc[test_idx]
    y_prob_test = _heuristic_probability(
        ordered_df.loc[test_idx],
        positive_columns=positive_columns,
        negative_columns=negative_columns,
    )

    return (
        {
            "model": {
                "type": "heuristic_fallback",
                "target": target_name,
                "positive_columns": positive_columns,
                "negative_columns": negative_columns,
            },
            "cv_roc_auc_mean": float("nan"),
            "cv_roc_auc_std": float("nan"),
            "temporal_test_roc_auc": _safe_roc_auc(y_test, y_prob_test),
            "split_strategy": f"{split_strategy}_heuristic_fallback",
            "train_size": int(len(y_train)),
            "test_size": int(len(y_test)),
            "fpr": [],
            "tpr": [],
            "precision": [],
            "recall": [],
            "x_test_index": list(test_idx),
            "y_prob_test": y_prob_test.tolist(),
        },
        _heuristic_probability(
            ordered_df, positive_columns=positive_columns, negative_columns=negative_columns
        ),
    )


def _validate_binary_target(y: pd.Series, target_name: str) -> None:
    if y.nunique() < 2:
        raise ValueError(
            f"Target '{target_name}' has a single class after preprocessing; cannot train a classifier."
        )


def train_and_score_models(df: pd.DataFrame, output_dir: Path) -> tuple[dict, dict, pd.DataFrame]:
    output_dir.mkdir(parents=True, exist_ok=True)
    work_df = df.copy().dropna(subset=["signup_date"])
    preprocessor, numeric_features, categorical_features = _build_preprocessor()
    feature_cols = numeric_features + categorical_features
    eval_df = work_df[feature_cols + ["signup_date", "is_churned", "next_purchase_30d"]].copy()

    churn_df = eval_df.dropna(subset=["is_churned"]).copy()
    churn_df["is_churned"] = churn_df["is_churned"].astype(int)
    _validate_binary_target(churn_df["is_churned"], "is_churned")
    if SKLEARN_AVAILABLE:
        x_churn = churn_df[feature_cols]
        churn_pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                (
                    "clf",
                    RandomForestClassifier(
                        n_estimators=280,
                        min_samples_leaf=5,
                        random_state=42,
                        class_weight="balanced",
                    ),
                ),
            ]
        )
        churn_results = _evaluate_pipeline_temporal(
            churn_pipeline, x_churn, churn_df["is_churned"], churn_df
        )
        churn_model = churn_results["model"]
        work_df["churn_probability"] = churn_model.predict_proba(work_df[feature_cols])[:, 1]
    else:
        churn_results, _ = _heuristic_model_summary(
            churn_df,
            churn_df["is_churned"],
            target_name="is_churned",
            positive_columns=["recency_days"],
            negative_columns=["frequency", "monetary", "arpu", "tenure_days"],
        )
        churn_model = churn_results["model"]
        work_df["churn_probability"] = _heuristic_probability(
            work_df,
            positive_columns=["recency_days"],
            negative_columns=["frequency", "monetary", "arpu", "tenure_days"],
        )

    next_df = eval_df.dropna(subset=["next_purchase_30d"]).copy()
    next_df["next_purchase_30d"] = next_df["next_purchase_30d"].astype(int)
    _validate_binary_target(next_df["next_purchase_30d"], "next_purchase_30d")
    if SKLEARN_AVAILABLE:
        x_next = next_df[feature_cols]
        next_purchase_pipeline = Pipeline(
            steps=[("preprocessor", preprocessor), ("clf", LogisticRegression(max_iter=1200))]
        )
        next_purchase_results = _evaluate_pipeline_temporal(
            next_purchase_pipeline, x_next, next_df["next_purchase_30d"], next_df
        )
        next_purchase_model = next_purchase_results["model"]
        work_df["next_purchase_probability"] = next_purchase_model.predict_proba(
            work_df[feature_cols]
        )[:, 1]
    else:
        next_purchase_results, _ = _heuristic_model_summary(
            next_df,
            next_df["next_purchase_30d"],
            target_name="next_purchase_30d",
            positive_columns=["frequency", "monetary", "avg_order_value", "arpu", "tenure_days"],
            negative_columns=["recency_days"],
        )
        next_purchase_model = next_purchase_results["model"]
        work_df["next_purchase_probability"] = _heuristic_probability(
            work_df,
            positive_columns=["frequency", "monetary", "avg_order_value", "arpu", "tenure_days"],
            negative_columns=["recency_days"],
        )

    _persist_model(churn_model, output_dir / "churn_model.joblib")
    _persist_model(next_purchase_model, output_dir / "next_purchase_model.joblib")
    work_df.to_csv(output_dir / "scored_customers.csv", index=False)
    report = {
        "churn": {
            "cv_roc_auc_mean": churn_results["cv_roc_auc_mean"],
            "cv_roc_auc_std": churn_results["cv_roc_auc_std"],
            "temporal_test_roc_auc": churn_results["temporal_test_roc_auc"],
            "split_strategy": churn_results["split_strategy"],
            "train_size": churn_results["train_size"],
            "test_size": churn_results["test_size"],
        },
        "next_purchase_30d": {
            "cv_roc_auc_mean": next_purchase_results["cv_roc_auc_mean"],
            "cv_roc_auc_std": next_purchase_results["cv_roc_auc_std"],
            "temporal_test_roc_auc": next_purchase_results["temporal_test_roc_auc"],
            "split_strategy": next_purchase_results["split_strategy"],
            "train_size": next_purchase_results["train_size"],
            "test_size": next_purchase_results["test_size"],
        },
    }
    with (output_dir / "metrics_report.json").open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    return churn_results, next_purchase_results, work_df
