import random
from datetime import date, timedelta

import streamlit as st

st.set_page_config(page_title="Executive Dashboard", layout="wide")

st.title("Revenue-Intelligence-Platform-Suite")
st.caption("Executive dashboard for revenue, retention, churn risk, and prioritization.")

st.sidebar.header("Scenario Controls")
segment = st.sidebar.selectbox("Segment", ["All", "Enterprise", "SMB", "Mid-Market"])
uplift = st.sidebar.slider("Retention uplift scenario (%)", min_value=0, max_value=30, value=8, step=1)
budget = st.sidebar.slider("Campaign budget (USD)", min_value=20_000, max_value=400_000, value=120_000, step=10_000)

seed = 42
random.seed(seed)

# Monthly trend for the last 12 months.
months = []
revenue_series = []
nrr_series = []
start = date.today().replace(day=1) - timedelta(days=330)
base_revenue = 2_050_000
base_nrr = 0.89
for i in range(12):
    month = (start + timedelta(days=30 * i)).strftime("%Y-%m")
    revenue = base_revenue + i * 42_000 + random.randint(-50_000, 50_000)
    nrr = round(base_nrr + (i * 0.002) + random.uniform(-0.01, 0.01), 3)
    months.append(month)
    revenue_series.append(max(revenue, 1_500_000))
    nrr_series.append(max(min(nrr, 0.98), 0.78))

total_revenue = revenue_series[-1]
current_nrr = nrr_series[-1]
gross_churn = round(1 - current_nrr, 3)
value_at_risk = int(total_revenue * gross_churn * 0.65)
expected_recovery = int(value_at_risk * (uplift / 100))
roi = round((expected_recovery - budget) / budget, 2)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Revenue (Current Month)", f"${total_revenue:,.0f}")
col2.metric("NRR", f"{current_nrr*100:.1f}%")
col3.metric("Gross Revenue Churn", f"{gross_churn*100:.1f}%")
col4.metric("Value at Risk", f"${value_at_risk:,.0f}")
col5.metric("Expected Recovery", f"${expected_recovery:,.0f}", delta=f"ROI {roi*100:.0f}%")

st.markdown("---")

left, right = st.columns([2, 1])
with left:
    st.subheader("Revenue Trend (12M)")
    st.line_chart({"Revenue": revenue_series})

with right:
    st.subheader("NRR Trend (12M)")
    st.line_chart({"NRR": [round(x * 100, 2) for x in nrr_series]})

st.markdown("---")

st.subheader("Top Retention Priorities")

accounts = []
for i in range(1, 31):
    acc_segment = random.choice(["Enterprise", "SMB", "Mid-Market"])
    if segment != "All" and acc_segment != segment:
        continue
    risk_score = round(random.uniform(0.45, 0.98), 2)
    account_value = random.randint(15_000, 220_000)
    recovery_score = int(account_value * risk_score * (uplift / 100))
    accounts.append(
        {
            "Account": f"ACC-{1000+i}",
            "Segment": acc_segment,
            "Risk Score": risk_score,
            "Revenue at Risk (USD)": account_value,
            "Expected Recovery (USD)": recovery_score,
            "Recommended Action": random.choice(
                ["CSM Call", "Pricing Review", "Offer Retention Pack", "Contract Renegotiation"]
            ),
        }
    )

accounts = sorted(accounts, key=lambda x: x["Expected Recovery (USD)"], reverse=True)
st.dataframe(accounts[:12], use_container_width=True)

st.markdown("---")

a, b, c = st.columns(3)
with a:
    st.subheader("Pipeline Health")
    st.write("- Data Contract Pass Rate: **97.2%**")
    st.write("- Pipeline Reliability: **98.4%**")
    st.write("- Data Freshness SLA: **On Track**")

with b:
    st.subheader("Model Health")
    st.write("- Churn Precision@K: **0.71**")
    st.write("- Drift Alert: **No critical drift**")
    st.write("- Last Retrain: **7 days ago**")

with c:
    st.subheader("Operating Cadence")
    st.write("- Weekly Business Review: **Active**")
    st.write("- Action Adoption Rate: **43%**")
    st.write("- Next Steering Meeting: **Monday**")

