import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(layout="wide")

# =========================================================
# TITLE
# =========================================================
st.title("🧠 TradePulse AI – Production Attrition Intelligence Platform")

# =========================================================
# SIDEBAR NAVIGATION (REAL APP FEEL)
# =========================================================
page = st.sidebar.radio("📂 Navigation", [
    "📌 Overview",
    "📊 Portfolio Dashboard",
    "📉 Driver Analytics",
    "💰 Revenue Impact",
    "🚨 RM Priority Queue",
    "🔍 Client 360 View"
])

# =========================================================
# INITIALIZATION BUTTON
# =========================================================
if "df" not in st.session_state:

    st.subheader("🚀 Start AI Agent")

    if st.button("Initialize System"):

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
            "Revenue": np.random.randint(50000, 5000000, n)
        })

        df["Churn_Flag"] = (
            (df["Transactions"] < 10) &
            (df["Interaction_Gap"] > 60) |
            (df["Wallet_Share"] < 0.3) |
            (df["Complaints"] > 5)
        ).astype(int)

        st.session_state.df = df
        st.success("✅ System initialized")

# =========================================================
# RUN MODEL PIPELINE
# =========================================================
if "df" in st.session_state:

    df = st.session_state.df.copy()

    features = [
        "Transactions","Transaction_Value","Complaints","SLA_Breach",
        "Interaction_Gap","RM_Contacts","Wallet_Share",
        "Digital_Usage","Product_Usage"
    ]

    model = RandomForestClassifier(n_estimators=120)
    model.fit(df[features], df["Churn_Flag"])

    df["Attrition_Score"] = (model.predict_proba(df[features])[:, 1] * 100).astype(int)

# =========================================================
# FEATURE ENGINEERING (IMPORTANT FOR SRS)
# =========================================================
    df["Engagement_Index"] = df["RM_Contacts"] / (df["Interaction_Gap"] + 1)
    df["Friction_Index"] = df["Complaints"] * df["SLA_Breach"]
    df["Wallet_Leakage_Index"] = (1 - df["Wallet_Share"]) * 100

# =========================================================
# RISK SEGMENTATION
# =========================================================
    def risk(x):
        if x < 35: return "Low"
        elif x < 55: return "Watch"
        elif x < 70: return "Medium"
        elif x < 85: return "High"
        else: return "Critical"

    df["Risk"] = df["Attrition_Score"].apply(risk)

# =========================================================
# PAGE 1 - OVERVIEW
# =========================================================
    if page == "📌 Overview":

        st.subheader("System Overview")

        st.markdown("""
        This AI engine predicts customer attrition using:
        - Behavioral signals (transactions)
        - Engagement signals (RM interaction)
        - Operational friction (complaints & SLA)
        - Financial signals (wallet share)
        - Digital activity
        
        Output:
        - Attrition Score (0–100)
        - Risk level
        - Business insights
        """)

# =========================================================
# PAGE 2 - PORTFOLIO DASHBOARD
# =========================================================
    elif page == "📊 Portfolio Dashboard":

        avg = int(df["Attrition_Score"].mean())
        risk_clients = len(df[df["Risk"].isin(["High","Critical"])])
        revenue = df[df["Risk"].isin(["High","Critical"])]["Revenue"].sum()

        c1, c2, c3 = st.columns(3)

        c1.metric("Avg Score", avg)
        c2.metric("High Risk Clients", risk_clients)
        c3.metric("Revenue at Risk", f"₹{revenue:,.0f}")

        st.write("👉 Interpretation:")
        if avg < 40:
            st.success("Healthy portfolio")
        elif avg < 70:
            st.warning("Moderate risk")
        else:
            st.error("High attrition risk")

        st.bar_chart(df["Risk"].value_counts())

# =========================================================
# PAGE 3 - DRIVER ANALYTICS
# =========================================================
    elif page == "📉 Driver Analytics":

        driver_df = pd.DataFrame({
            "Driver": ["Friction", "Engagement", "Wallet Leakage"],
            "Score": [
                df["Friction_Index"].mean(),
                df["Engagement_Index"].mean(),
                df["Wallet_Leakage_Index"].mean()
            ]
        })

        st.bar_chart(driver_df.set_index("Driver"))

        st.write("👉 Shows root causes of attrition")

# =========================================================
# PAGE 4 - REVENUE IMPACT
# =========================================================
    elif page == "💰 Revenue Impact":

        rev = df.groupby("Risk")["Revenue"].sum()
        st.bar_chart(rev)

        st.write("👉 Financial exposure due to attrition")

# =========================================================
# PAGE 5 - RM PRIORITY
# =========================================================
    elif page == "🚨 RM Priority Queue":

        top = df.sort_values(by="Attrition_Score", ascending=False).head(20)
        st.dataframe(top)

        st.write("👉 These clients need immediate attention")

# =========================================================
# PAGE 6 - CLIENT VIEW
# =========================================================
    elif page == "🔍 Client 360 View":

        selected = st.selectbox("Select Client", df["Client_ID"])
        client = df[df["Client_ID"] == selected].iloc[0]

        st.write(client)

        st.subheader("Insights")

        if client["Transactions"] < 10:
            st.write("• Declining transactions")
        if client["Complaints"] > 5:
            st.write("• High complaints")
        if client["Interaction_Gap"] > 60:
            st.write("• Low engagement")
        if client["Wallet_Share"] < 0.4:
            st.write("• Wallet leakage")

        st.subheader("Action")

        if client["Attrition_Score"] > 80:
            st.error("Immediate intervention needed")
        else:
            st.info("Monitor client")

else:
    st.warning("Initialize system from Overview page")AI Agent to start")
