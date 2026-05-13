import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(layout="wide")

# ======================================================
# HEADER (LIVE SYSTEM)
# ======================================================
st.title("🏦 TradePulse AI – Live Attrition Monitoring System")
st.success("✅ System Status: LIVE | Monitoring 1,500 Active Clients")

# ======================================================
# SIMULATE LIVE DATA (AUTO LOAD)
# ======================================================
@st.cache_data
def generate_data():

    np.random.seed(42)
    n = 1500

    df = pd.DataFrame({
        "Client_ID": range(10001, 10001+n),
        "Transactions_30d": np.random.randint(1, 80, n),
        "Transactions_90d": np.random.randint(50, 200, n),
        "Transaction_Value": np.random.randint(1000, 100000, n),
        "Complaints_90d": np.random.randint(0, 10, n),
        "SLA_Breach_Rate": np.random.uniform(0, 1, n),
        "Interaction_Days": np.random.randint(1, 180, n),
        "RM_Contacts": np.random.randint(0, 15, n),
        "Wallet_Share": np.random.uniform(0.1, 1, n),
        "Digital_Usage": np.random.randint(0, 50, n),
        "Revenue": np.random.randint(50000, 5000000, n)
    })

    # Behavioral change simulation
    df["Transaction_Trend"] = df["Transactions_30d"] - (df["Transactions_90d"] / 3)

    # Label (simulated attrition pattern)
    df["Churn_Flag"] = (
        (df["Transaction_Trend"] < -10) |
        (df["Wallet_Share"] < 0.3) |
        (df["Complaints_90d"] > 5) |
        (df["Interaction_Days"] > 60)
    ).astype(int)

    return df


df = generate_data()

# ======================================================
# MODEL (RUNS AUTOMATICALLY)
# ======================================================
features = [
    "Transactions_30d", "Transaction_Value", "Complaints_90d",
    "SLA_Breach_Rate", "Interaction_Days",
    "RM_Contacts", "Wallet_Share",
    "Digital_Usage", "Transaction_Trend"
]

model = RandomForestClassifier(n_estimators=100)
model.fit(df[features], df["Churn_Flag"])

df["Attrition_Probability"] = model.predict_proba(df[features])[:, 1]
df["Score"] = (df["Attrition_Probability"] * 100).astype(int)

# ======================================================
# RISK SEGMENT
# ======================================================
def risk(score):
    if score < 35: return "Low"
    elif score < 55: return "Watch"
    elif score < 70: return "Medium"
    elif score < 85: return "High"
    else: return "Critical"

df["Risk"] = df["Score"].apply(risk)

# ======================================================
# SIDEBAR NAVIGATION
# ======================================================
page = st.sidebar.radio("Navigation", [
    "📊 Executive Dashboard",
    "🚨 Live Alerts",
    "📉 Driver Analysis",
    "💰 Revenue at Risk",
    "📋 Client Portfolio",
    "🔍 Client Deep Dive"
])

# ======================================================
# 📊 EXECUTIVE DASHBOARD
# ======================================================
if page == "📊 Executive Dashboard":

    st.subheader("Portfolio Health Overview")

    avg_score = int(df["Score"].mean())
    high_risk = len(df[df["Risk"].isin(["High","Critical"])])
    revenue_risk = df[df["Risk"].isin(["High","Critical"])]["Revenue"].sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Avg Attrition Score", avg_score)
    col2.metric("High Risk Clients", high_risk)
    col3.metric("Critical Clients", len(df[df["Risk"]=="Critical"]))
    col4.metric("Revenue at Risk", f"₹{revenue_risk:,.0f}")

    st.write("### 🧠 Interpretation")

    if avg_score < 40:
        st.success("Portfolio Stable")
    elif avg_score < 70:
        st.warning("Moderate Risk Emerging")
    else:
        st.error("High Attrition Risk Detected")

    st.write("### 📉 Risk Distribution")
    st.bar_chart(df["Risk"].value_counts())

# ======================================================
# 🚨 LIVE ALERTS
# ======================================================
elif page == "🚨 Live Alerts":

    st.subheader("Real-Time Attrition Alerts")

    alerts = df[df["Risk"].isin(["High","Critical"])].sort_values(by="Score", ascending=False).head(20)

    st.dataframe(alerts)

    st.warning("👉 These clients require immediate RM intervention")

# ======================================================
# 📉 DRIVER ANALYSIS
# ======================================================
elif page == "📉 Driver Analysis":

    st.subheader("Root Cause Analysis")

    drivers = {
        "Transaction Drop": len(df[df["Transaction_Trend"] < -10]),
        "High Complaints": len(df[df["Complaints_90d"] > 5]),
        "Low Engagement": len(df[df["Interaction_Days"] > 60]),
        "Wallet Leakage": len(df[df["Wallet_Share"] < 0.4])
    }

    driver_df = pd.DataFrame(list(drivers.items()), columns=["Driver", "Clients"])

    st.bar_chart(driver_df.set_index("Driver"))

# ======================================================
# 💰 REVENUE
# ======================================================
elif page == "💰 Revenue at Risk":

    st.subheader("Revenue Exposure")

    st.bar_chart(df.groupby("Risk")["Revenue"].sum())

    st.write("👉 Indicates financial impact of attrition")

# ======================================================
# 📋 PORTFOLIO
# ======================================================
elif page == "📋 Client Portfolio":

    st.subheader("Active Client Portfolio")

    st.dataframe(df)

# ======================================================
# 🔍 CLIENT VIEW
# ======================================================
elif page == "🔍 Client Deep Dive":

    selected = st.selectbox("Select Client", df["Client_ID"])
    client = df[df["Client_ID"] == selected].iloc[0]

    st.write(client)

    st.subheader("🧠 Insight Summary")

    if client["Transaction_Trend"] < -10:
        st.write("• Declining transactions detected")
    if client["Complaints_90d"] > 5:
        st.write("• High complaints → dissatisfaction")
    if client["Interaction_Days"] > 60:
        st.write("• Low RM engagement")
    if client["Wallet_Share"] < 0.4:
        st.write("• Wallet share erosion")

    st.subheader("🎯 Recommended Action")

    if client["Score"] > 85:
        st.error("Immediate escalation required")
    else:
        st.warning("RM follow-up required")tem from Overview page to start the AI Agent")
