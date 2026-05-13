import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(layout="wide")

# -------------------------------------------------------
# HEADER
# -------------------------------------------------------
st.title("🧠 TradePulse AI – Attrition Intelligence Dashboard")
st.markdown("### Predict | Explain | Act")

# -------------------------------------------------------
# INITIALIZE DATA
# -------------------------------------------------------
if st.button("🚀 Initialize System"):

    np.random.seed(42)
    n = 1500

    df = pd.DataFrame({
        "Client_ID": range(1, n+1),
        "Transactions": np.random.randint(1, 80, n),
        "Transaction_Value": np.random.randint(1000, 100000, n),
        "Complaints": np.random.randint(0, 10, n),
        "SLA_Breach": np.random.uniform(0, 1, n),
        "Interaction_Gap": np.random.randint(1, 180, n),
        "RM_Contacts": np.random.randint(0, 15, n),
        "Wallet_Share": np.random.uniform(0.1, 1, n),
        "Digital_Usage": np.random.randint(0, 50, n),
        "Product_Usage": np.random.randint(1, 12, n),
        "Revenue": np.random.randint(50000, 5000000, n)  # ✅ FIX ADDED
    })

    # Simulated churn logic
    df["Churn_Flag"] = (
        (df["Transactions"] < 10) &
        (df["Interaction_Gap"] > 60) |
        (df["Wallet_Share"] < 0.3) |
        (df["Complaints"] > 5)
    ).astype(int)

    st.session_state.df = df

# -------------------------------------------------------
# MAIN APP
# -------------------------------------------------------
if "df" in st.session_state:

    df = st.session_state.df.copy()

    # ---------------------------------------------------
    # FEATURE & MODEL
    # ---------------------------------------------------
    features = [
        "Transactions",
        "Transaction_Value",
        "Complaints",
        "SLA_Breach",
        "Interaction_Gap",
        "RM_Contacts",
        "Wallet_Share",
        "Digital_Usage",
        "Product_Usage"
    ]

    model = RandomForestClassifier(n_estimators=120)
    model.fit(df[features], df["Churn_Flag"])

    df["Probability"] = model.predict_proba(df[features])[:, 1]
    df["Score"] = (df["Probability"] * 100).astype(int)

    # ---------------------------------------------------
    # RISK SEGMENT
    # ---------------------------------------------------
    def risk(score):
        if score < 35: return "Low"
        elif score < 55: return "Watch"
        elif score < 70: return "Medium"
        elif score < 85: return "High"
        else: return "Critical"

    df["Risk"] = df["Score"].apply(risk)

    # ---------------------------------------------------
    # NAVIGATION
    # ---------------------------------------------------
    page = st.sidebar.radio("🔍 Navigation", [
        "Executive Overview",
        "Risk Analytics",
        "RM Priority View",
        "Client 360° View"
    ])

# -------------------------------------------------------
# EXECUTIVE OVERVIEW
# -------------------------------------------------------
    if page == "Executive Overview":

        st.subheader("📊 Portfolio Overview")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Clients", len(df))
        col2.metric("Avg Risk Score", int(df["Score"].mean()))
        col3.metric("High Risk Clients", len(df[df["Risk"].isin(["High","Critical"])]))

        # ✅ SAFE REVENUE CALCULATION FIX
        if "Revenue" in df.columns:
            revenue_risk = df[df["Risk"].isin(["High", "Critical"])]["Revenue"].sum()
            col4.metric("Revenue at Risk", f"₹{revenue_risk:,.0f}")
        else:
            col4.metric("Revenue at Risk", "Not available")

        st.markdown("### 🔴 Risk Distribution")
        st.bar_chart(df["Risk"].value_counts())

        st.markdown("### 💰 Revenue Contribution")
        st.bar_chart(df.groupby("Risk")["Revenue"].sum())

# -------------------------------------------------------
# RISK ANALYTICS
# -------------------------------------------------------
    elif page == "Risk Analytics":

        st.subheader("📈 Behavior Insights")

        st.line_chart(df.sort_values("Client_ID")["Transactions"])

        st.subheader("⚠️ Risk Indicators")

        col1, col2 = st.columns(2)

        with col1:
            st.write("High Complaints:", len(df[df["Complaints"] > 5]))
            st.write("Low Engagement:", len(df[df["Interaction_Gap"] > 60]))

        with col2:
            st.write("Low Wallet Share:", len(df[df["Wallet_Share"] < 0.4]))
            st.write("Digital Drop:", len(df[df["Digital_Usage"] < 5]))

# -------------------------------------------------------
# RM PRIORITY
# -------------------------------------------------------
    elif page == "RM Priority View":

        st.subheader("🚨 Top Risk Clients")

        priority = df.sort_values(by="Score", ascending=False).head(15)
        st.dataframe(priority)

        st.markdown("### 🎯 RM Action Strategy")
        st.write("""
        • Immediate outreach  
        • Pricing discussion  
        • Relationship strengthening  
        """)

# -------------------------------------------------------
# CLIENT VIEW
# -------------------------------------------------------
    elif page == "Client 360° View":

        st.subheader("🔍 Client Analysis")

        selected = st.selectbox("Select Client", df["Client_ID"])
        client = df[df["Client_ID"] == selected].iloc[0]

        col1, col2 = st.columns(2)

        with col1:
            st.write("### Client Profile")
            st.write(client)

        with col2:
            st.write("### AI Insights")

            insights = []

            if client["Transactions"] < 10:
                insights.append("Transactions declining → migration risk")

            if client["Complaints"] > 5:
                insights.append("High complaints → dissatisfaction")

            if client["Interaction_Gap"] > 60:
                insights.append("Low engagement")

            if client["Wallet_Share"] < 0.4:
                insights.append("Wallet share erosion")

            if client["Digital_Usage"] < 5:
                insights.append("Digital disengagement")

            for i in insights:
                st.write("•", i)

            st.write("### 🎯 Action")

            if client["Score"] > 85:
                st.error("Immediate escalation")
            elif client["Score"] > 70:
                st.warning("High RM priority")
            elif client["Score"] > 55:
                st.info("Monitor closely")
            else:
                st.success("Healthy")

else:
    st.info("Click 'Initialize System' to start")
