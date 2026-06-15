import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

st.set_page_config(
    page_title="Fraud Detection Dashboard",
    layout="wide"
)

st.title("🚨 Real-Time Fraud Detection Dashboard")

engine = create_engine(
    "postgresql://frauduser:fraudpass@localhost:5432/frauddb"
)

transactions = pd.read_sql(
    "SELECT * FROM transactions ORDER BY processed_time DESC",
    engine
)

alerts = pd.read_sql(
    "SELECT * FROM fraud_alerts ORDER BY alert_time DESC",
    engine
)

critical_count = len(
    transactions[
        transactions["risk_level"] == "CRITICAL"
    ]
)

high_count = len(
    transactions[
        transactions["risk_level"] == "HIGH"
    ]
)

medium_count = len(
    transactions[
        transactions["risk_level"] == "MEDIUM"
    ]
)

low_count = len(
    transactions[
        transactions["risk_level"] == "LOW"
    ]
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Transactions",
    len(transactions)
)

col2.metric(
    "Critical",
    critical_count
)

col3.metric(
    "High",
    high_count
)

col4.metric(
    "Medium",
    medium_count
)

risk_counts = transactions["risk_level"].value_counts()

chart_df = risk_counts.reset_index()
chart_df.columns = ["Risk Level", "Count"]

st.bar_chart(
    chart_df.set_index("Risk Level")
)

st.subheader("Transactions")

st.dataframe(
    transactions,
    use_container_width=True
)

st.subheader("Fraud Alerts")

st.dataframe(
    alerts,
    use_container_width=True
)

st.subheader("Top High Risk Transactions")

high_risk = transactions[
    transactions["risk_level"].isin(
        ["HIGH", "CRITICAL"]
    )
]

st.dataframe(
    high_risk,
    use_container_width=True
)