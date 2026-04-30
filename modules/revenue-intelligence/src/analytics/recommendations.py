from __future__ import annotations

import pandas as pd


def build_recommendations(ltv_df: pd.DataFrame, cac_df: pd.DataFrame) -> pd.DataFrame:
    channel_cac = cac_df[["channel", "cac"]].copy()
    out = ltv_df.merge(channel_cac, on="channel", how="left").fillna({"cac": 0})
    out["ltv_cac_ratio"] = out["ltv"] / out["cac"].replace(0, 1)

    ltv_top = out["ltv"].quantile(0.7)
    ltv_low = out["ltv"].quantile(0.3)
    cac_median = out["cac"].median()

    def map_action(row: pd.Series) -> str:
        if row["churn_probability"] > 0.7:
            return "Retention Campaign"
        if row["ltv"] > ltv_top and row["churn_probability"] < 0.4:
            return "Upsell Offer"
        if row["ltv"] < ltv_low and row["cac"] > cac_median:
            return "Reduce Acquisition Spend"
        return "Nurture"

    out["recommended_action"] = out.apply(map_action, axis=1)
    out["strategic_score"] = (
        0.45 * out["ltv"].rank(pct=True)
        + 0.35 * (1 - out["churn_probability"])
        + 0.2 * out["next_purchase_probability"]
    )
    out = out.sort_values("strategic_score", ascending=False)
    cols = [
        "customer_id",
        "channel",
        "segment",
        "ltv",
        "cac",
        "ltv_cac_ratio",
        "churn_probability",
        "next_purchase_probability",
        "strategic_score",
        "recommended_action",
    ]
    return out[cols]
