import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(layout="wide")

st.title("🧠 TradePulse AI - Full Attrition Prediction Platform")

# ----------------------------------------------------
# INITIALIZE LARGE DATASET
# ----------------------------------------------------
if st.button("🚀 Initialize AI System"):

    np.random.seed(42)

    n = 1200  # LARGE dataset

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
        "Product_Usage": np.random.randint(1, 10, n)
    })

    # ---------------------------------------
    # CREATE REALISTIC CHURN TARGET
    # ---------------------------------------
    df["Churn_Flag"] = (
        (df["Transactions"] < 10) &
        (df["Interaction_Gap"] > 60) |
        (df["Wallet_Share"] < 0.3) |
        (df["Complaints"] > 5)
    ).astype(int)

    st.session_state.df = df

# ----------------------------------------------------
# MODEL + DASHBOARD
# ----------------------------------------------------
if "df" in st.session_state:

    df = st.session_state.df.copy()

    # ------------------------------------------------
    # MODEL TRAINING (REAL PREDICTION)
    # ------------------------------------------------
    features = [
        "Transactions", "Transaction_Value", "Complaints",
        "SLA_Breach", "Interaction_Gap", "RM_Contacts",
        "Wallet_Share", "Digital_Usage", "Product_Usage"
    ]

    X = df[features]
    y = df["Churn_Flag"]

    model = RandomForestClassifier(n_estimators=120)
    model.fit(X, y)

    # ------------------------------------------------
    # PREDICTION
    # ------------------------------------------------
    df["Churn_Probability"] = model.predict_proba(X)[:, 1]
    df["Score"] = (df["Churn_Probability"] * 100).astype(int)

    # ------------------------------------------------
    # RISK SEGMENT
    # ------------------------------------------------
    def risk(score):
        if score < 35: return "Low"
        elif score < 55: return "Watch"
        elif score < 70: return "Medium"
        elif score < 85: return "High"
        else: return "Critical"

    df["Risk"] = df["Score"].apply(risk)

    # ------------------------------------------------
    # PAGE NAVIGATION
    # ------------------------------------------------
    page = st.sidebar.radio("Navigation", [
        "Overview",
        "Portfolio",
        "High Risk",
        "Client Drilldown"
    ])

# ----------------------------------------------------
# PAGE 1 - OVERVIEW
# ----------------------------------------------------
    if page == "Overview":

        st.subheader("📊 Portfolio Overview")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Clients", len(df))
        col2.metric("Avg Score", int(df["Score"].mean()))
        col3.metric("High Risk Clients", len(df[df["Risk"].isin(["High","Critical"])]))
        col4.metric("Critical", len(df[df["Risk"]=="Critical"]))

        st.subheader("🔴 Risk Distribution")
        st.bar_chart(df["Risk"].value_counts())

# ----------------------------------------------------
# PAGE 2 - FULL PORTFOLIO
# ----------------------------------------------------
    elif page == "Portfolio":

        st.subheader("📋 Full Customer Portfolio")

        st.dataframe(df)

# ----------------------------------------------------
# PAGE 3 - HIGH RISK
# ----------------------------------------------------
    elif page == "High Risk":

        st.subheader("🚨 Priority Customer List")

        high = df[df["Risk"].isin(["High", "Critical"])]

        st.dataframe(high.sort_values(by="Score", ascending=False).head(50))

# ----------------------------------------------------
# PAGE 4 - DRILLDOWN
# ----------------------------------------------------
    elif page == "Client Drilldown":

        st.subheader("🔍 Client Analysis")

        selected = st.selectbox("Select Client", df["Client_ID"])

        client = df[df["Client_ID"] == selected].iloc[0]

        st.write("### Client Details")
        st.write(client)

        # ----------------------------------------
        # FEATURE IMPORTANCE (Explainability)
        # ----------------------------------------
        st.write("### AI Feature Importance")

        importance = pd.DataFrame({
            "Feature": features,
            "Importance": model.feature_importances_
        }).sort_values(by="Importance", ascending=False)

        st.dataframe(importance)

        # ----------------------------------------
        # DRIVERS
        # ----------------------------------------
        st.write("### Key Risk Drivers")

        drivers = []

        if client["Transactions"] < 10:
            drivers.append("Low transaction activity")
        if client["Complaints"] > 5:
            drivers.append("High complaints")
        if client["Interaction_Gap"] > 60:
            drivers.append("Low engagement")
        if client["Wallet_Share"] < 0.4:
            drivers.append("Wallet share erosion")
        if client["Digital_Usage"] < 5:
            drivers.append("Digital disengagement")

        for d in drivers:
            st.write("•", d)

        # ----------------------------------------
        # ACTION ENGINE
        # ----------------------------------------
        st.write("### 🎯 Recommended Action")

        if client["Score"] > 85:
            st.error("Immediate escalation (RM + pricing)")
        elif client["Score"] > 70:
            st.warning("High priority RM intervention")
        elif client["Score"] > 55:
            st.info("Monitor closely")
        else:
            st.success("Healthy client")

else:
    st.info("Click 'Initialize AI System' to start")
