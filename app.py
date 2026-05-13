import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(layout="wide")

st.title("🏦 TradePulse AI – Attrition Intelligence Platform")

# =====================================================
# DATA GENERATION
# =====================================================
@st.cache_data
def generate_data():

    np.random.seed(42)
    n = 500

    df = pd.DataFrame({
        "Client_ID": range(10001, 10001+n),

        # Trade
        "Trade_Decline": np.random.randint(-80, 40, n),

        # Treasury
        "Wallet_Share": np.random.uniform(0.1, 1, n),

        # CRM
        "Interaction_Days": np.random.randint(1, 120, n),

        # Operations
        "Complaints": np.random.randint(0, 10, n),

        # Digital
        "Digital_Usage": np.random.randint(0, 50, n),

        # Revenue
        "Revenue": np.random.randint(50000, 2000000, n)
    })

    # Target
    df["Churn"] = (
        (df["Trade_Decline"] < -40) |
        (df["Wallet_Share"] < 0.4) |
        (df["Complaints"] > 5) |
        (df["Interaction_Days"] > 60)
    ).astype(int)

    return df

df = generate_data()

# =====================================================
# MODEL
# =====================================================
features = [
    "Trade_Decline",
    "Wallet_Share",
    "Interaction_Days",
    "Complaints",
    "Digital_Usage"
]

model = RandomForestClassifier(n_estimators=100)
model.fit(df[features], df["Churn"])

df["Score"] = (model.predict_proba(df[features])[:,1] * 100).astype(int)

# Risk segment
def risk(x):
    if x < 35: return "Low"
    elif x < 55: return "Watch"
    elif x < 70: return "Medium"
    elif x < 85: return "High"
    else: return "Critical"

df["Risk"] = df["Score"].apply(risk)

# =====================================================
# NAVIGATION
# =====================================================
page = st.sidebar.radio("Navigation", [
    "Executive Summary",
    "Client Signals",
    "Alerts",
    "RM Workflow",
    "Client View"
])

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================
if page == "Executive Summary":

    st.subheader("Portfolio Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Avg Score", int(df["Score"].mean()))
    col2.metric("High Risk", len(df[df["Risk"].isin(["High","Critical"])]))
    col3.metric("Revenue at Risk", f"₹{df[df['Risk'].isin(['High','Critical'])]['Revenue'].sum():,.0f}")

    st.write("### Insights")

    st.write(f"• {len(df[df['Trade_Decline'] < -40])} clients with trade decline")
    st.write(f"• {len(df[df['Wallet_Share'] < 0.4])} clients losing wallet share")
    st.write(f"• {len(df[df['Complaints'] > 5])} clients with complaints")
    st.write(f"• {len(df[df['Interaction_Days'] > 60])} disengaged clients")

# =====================================================
# CLIENT SIGNALS
# =====================================================
elif page == "Client Signals":

    st.subheader("Client-Level Signals")

    st.dataframe(df)

# =====================================================
# ALERTS
# =====================================================
elif page == "Alerts":

    st.subheader("High Risk Alerts")

    alerts = df[df["Risk"].isin(["High","Critical"])].sort_values(by="Score", ascending=False)

    st.dataframe(alerts.head(15))

# =====================================================
# RM WORKFLOW
# =====================================================
elif page == "RM Workflow":

    st.subheader("RM Action Table")

    df["RM_Status"] = np.random.choice(["Pending","Contacted","Resolved"], size=len(df))

    st.dataframe(df[[
        "Client_ID",
        "Risk",
        "Score",
        "RM_Status",
        "Revenue"
    ]].sort_values(by="Score", ascending=False))

# =====================================================
# CLIENT VIEW
# =====================================================
elif page == "Client View":

    st.subheader("Client Deep Dive")

    client_id = st.selectbox("Select Client", df["Client_ID"])
    client = df[df["Client_ID"] == client_id].iloc[0]

    st.write(client)

    st.subheader("Insights")

    if client["Trade_Decline"] < -40:
        st.write("• Trade decline")

    if client["Wallet_Share"] < 0.4:
        st.write("• Wallet loss")

    if client["Complaints"] > 5:
        st.write("• High complaints")

    if client["Interaction_Days"] > 60:
        st.write("• Low engagement")

    st.subheader("Action")

    if client["Risk"] == "Critical":
        st.error("Immediate escalation")
    elif client["Risk"] == "High":
        st.warning("RM intervention needed")
    else:
        st.success("Monitor")
