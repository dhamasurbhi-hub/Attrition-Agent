import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(layout="wide")

st.title("🏦 TradePulse AI – Enterprise Attrition Intelligence Platform")
st.caption("Live Multi-System Monitoring | Predict → Explain → Act")

# =========================================================
# ✅ GENERATE MULTI-SYSTEM DATA (AS PER SRS)
# =========================================================
@st.cache_data
def generate_data():
    np.random.seed(42)
    n = 1000

    df = pd.DataFrame({
        "Client_ID": range(10001, 10001+n),

        # 🔵 Trade System
        "LC_Volume": np.random.randint(20, 200, n),
        "Trade_Decline": np.random.randint(-80, 40, n),

        # 🟢 Treasury System
        "FX_Conversion": np.random.uniform(0.2, 1, n),
        "Wallet_Share": np.random.uniform(0.1, 1, n),

        # 🔴 CRM / RM System
        "RM_Contacts": np.random.randint(0, 12, n),
        "Interaction_Days": np.random.randint(1, 120, n),

        # 🟡 Operations
        "Complaints": np.random.randint(0, 10, n),
        "SLA_Breach": np.random.uniform(0, 1, n),

        # 🟣 Digital
        "Digital_Usage": np.random.randint(0, 50, n),

        # 💰 Revenue
        "Revenue": np.random.randint(50000, 5000000, n)
    })

    # ===================================================
    # ✅ TARGET CREATION (SIMULATED ATTRITION BEHAVIOR)
    # ===================================================
    df["Churn"] = (
        (df["Trade_Decline"] < -40) |
        (df["Wallet_Share"] < 0.4) |
        (df["Complaints"] > 5) |
        (df["Interaction_Days"] > 60)
    ).astype(int)

    return df

df = generate_data()

# =========================================================
# ✅ MODEL (REAL PREDICTION)
# =========================================================
features = [
    "LC_Volume","Trade_Decline","FX_Conversion",
    "Wallet_Share","RM_Contacts","Interaction_Days",
    "Complaints","SLA_Breach","Digital_Usage"
]

model = RandomForestClassifier(n_estimators=120)
model.fit(df[features], df["Churn"])

df["Attrition_Score"] = (model.predict_proba(df[features])[:,1] * 100).astype(int)

# =========================================================
# ✅ RISK SEGMENTATION
# =========================================================
def risk(x):
    if x < 35: return "Low"
    elif x < 55: return "Watch"
    elif x < 70: return "Medium"
    elif x < 85: return "High"
    else: return "Critical"

df["Risk"] = df["Attrition_Score"].apply(risk)

# =========================================================
# ✅ SIDEBAR NAVIGATION (FULL APP STRUCTURE)
# =========================================================
page = st.sidebar.radio("📂 Navigate", [
    "📊 Executive Dashboard",
    "🔵 Trade Analysis",
    "🟢 Treasury Leakage",
    "🔴 CRM Engagement",
    "🟡 Operations (Friction)",
    "🟣 Digital Behavior",
    "🚨 Alerts & Workflow",
    "🔍 Client 360"
])

# =========================================================
# 📊 EXECUTIVE DASHBOARD
# =========================================================
if page == "📊 Executive Dashboard":

    st.subheader("Portfolio Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Clients", len(df))
    col2.metric("Avg Score", int(df["Attrition_Score"].mean()))
    col3.metric("High Risk", len(df[df["Risk"].isin(["High","Critical"])]))
    col4.metric("Revenue Risk", f"₹{df[df['Risk'].isin(['High','Critical'])]['Revenue'].sum():,.0f}")

    st.markdown("### 📉 Risk Distribution")
    st.plotly_chart(px.bar(df["Risk"].value_counts()))

    st.markdown("### 💰 Revenue Exposure")
    st.plotly_chart(px.bar(df.groupby("Risk")["Revenue"].sum()))

# =========================================================
# 🔵 TRADE ANALYSIS
# =========================================================
elif page == "🔵 Trade Analysis":

    st.subheader("Trade Behavior Insights")

    st.plotly_chart(px.histogram(df, x="Trade_Decline", title="Trade Decline Distribution"))

    st.write("""
    👉 Falling LC volumes and trade decline indicate migration to competitors  
    """)

# =========================================================
# 🟢 TREASURY
# =========================================================
elif page == "🟢 Treasury Leakage":

    st.subheader("Treasury Leakage Analysis")

    st.plotly_chart(px.histogram(df, x="Wallet_Share"))

    st.write("""
    👉 Low wallet share = revenue shifting to other banks  
    """)

# =========================================================
# 🔴 CRM
# =========================================================
elif page == "🔴 CRM Engagement":

    st.subheader("RM Engagement")

    st.plotly_chart(px.scatter(df, x="Interaction_Days", y="RM_Contacts"))

    st.write("""
    👉 High interaction gap + low contact frequency = disengagement  
    """)

# =========================================================
# 🟡 OPERATIONS
# =========================================================
elif page == "🟡 Operations (Friction)":

    st.subheader("Service Friction")

    st.plotly_chart(px.scatter(df, x="Complaints", y="SLA_Breach"))

    st.write("""
    👉 High complaints + SLA breaches → service dissatisfaction  
    """)

# =========================================================
# 🟣 DIGITAL
# =========================================================
elif page == "🟣 Digital Behavior":

    st.subheader("Digital Usage")

    st.plotly_chart(px.histogram(df, x="Digital_Usage"))

    st.write("""
    👉 Drop in digital usage → early disengagement signal  
    """)

# =========================================================
# 🚨 ALERTS
# =========================================================
elif page == "🚨 Alerts & Workflow":

    st.subheader("Live Alert Feed")

    alerts = df[df["Risk"].isin(["High","Critical"])].sort_values(by="Attrition_Score", ascending=False).head(15)

    for _, row in alerts.iterrows():
        st.error(f"Client {row['Client_ID']} | Score {row['Attrition_Score']} → Immediate Action")

# =========================================================
# 🔍 CLIENT 360
# =========================================================
elif page == "🔍 Client 360":

    st.subheader("Client Deep Dive")

    client_id = st.selectbox("Select Client", df["Client_ID"])
    client = df[df["Client_ID"] == client_id].iloc[0]

    col1, col2 = st.columns(2)

    with col1:
        st.write(client)

    with col2:
        st.write("### AI Insights")

        if client["Trade_Decline"] < -40:
            st.write("• Trade volume dropping")
        if client["Wallet_Share"] < 0.4:
            st.write("• Wallet leakage")
        if client["Complaints"] > 5:
            st.write("• High complaints")
        if client["Interaction_Days"] > 60:
            st.write("• Low engagement")

        st.write("### Action")

        if client["Attrition_Score"] > 85:
            st.error("Immediate escalation required")
        else:
            st.warning("RM follow-up needed")
