import pandas as pd
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine
from streamlit_autorefresh import st_autorefresh

# Auto refresh every 5 seconds
st_autorefresh(
    interval=5000,
    key="fraud_dashboard_refresh"
)

st.set_page_config(
    page_title="Fraud Detection Dashboard",
    layout="wide"
)

st.title("🚨 Real-Time Fraud Detection Dashboard")

# Database Connection
engine = create_engine(
    "postgresql://frauduser:fraudpass@localhost:5432/frauddb"
)

# Load Data
transactions = pd.read_sql(
    """
    SELECT *
    FROM transactions
    ORDER BY processed_time DESC
    """,
    engine
)

alerts = pd.read_sql(
    """
    SELECT *
    FROM fraud_alerts
    ORDER BY alert_time DESC
    """,
    engine
)

# Metrics
total_transactions = len(transactions)

fraud_alert_count = len(alerts)

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

# KPI Cards
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Transactions",
    total_transactions
)

col2.metric(
    "Fraud Alerts",
    fraud_alert_count
)

col3.metric(
    "Critical",
    critical_count
)

col4.metric(
    "High",
    high_count
)

col5.metric(
    "Medium",
    medium_count
)

st.divider()

# Risk Distribution
risk_counts = transactions["risk_level"].value_counts()

chart_df = risk_counts.reset_index()
chart_df.columns = ["Risk Level", "Count"]

col_left, col_right = st.columns(2)

with col_left:

    st.subheader("Risk Distribution")

    st.bar_chart(
        chart_df.set_index("Risk Level")
    )

with col_right:

    st.subheader("Risk Breakdown")

    fig = px.pie(
        chart_df,
        values="Count",
        names="Risk Level",
        hole=0.4
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# Recent Transactions
st.subheader("Latest Transactions")

st.dataframe(
    transactions.head(25),
    use_container_width=True
)

st.divider()

# Recent Alerts
st.subheader("Recent Fraud Alerts")

st.dataframe(
    alerts.head(25),
    use_container_width=True
)

st.divider()

# High Risk Transactions
st.subheader("High Risk Transactions")

high_risk = transactions[
    transactions["risk_level"].isin(
        ["HIGH", "CRITICAL"]
    )
]

st.dataframe(
    high_risk,
    use_container_width=True
)

st.success(
    f"Dashboard refreshed successfully. "
    f"Tracking {total_transactions} transactions."
)