import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(layout="wide")

# -------------------------------------------------------
# HEADER
# -------------------------------------------------------
st.title("🧠 TradePulse AI – Attrition Intelligence Platform")
st.markdown("### Predict • Explain • Act")

# -------------------------------------------------------
# INITIALIZE DATA
# -------------------------------------------------------
if st.button("🚀 Initialize AI System"):

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

    # Simulated churn pattern
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
    # MODEL
    # ---------------------------------------------------
    features = [
        "Transactions", "Transaction_Value", "Complaints",
        "SLA_Breach", "Interaction_Gap", "RM_Contacts",
        "Wallet_Share", "Digital_Usage", "Product_Usage"
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
        "Driver Analytics",
        "RM Priority View",
        "Client 360° View"
    ])

# -------------------------------------------------------
# PAGE 1 - EXECUTIVE OVERVIEW
# -------------------------------------------------------
    if page == "Executive Overview":

        st.subheader("📊 Portfolio Overview")

        total_clients = len(df)
        avg_score = int(df["Score"].mean())
        high_risk = len(df[df["Risk"].isin(["High", "Critical"])])
        revenue_risk = df[df["Risk"].isin(["High", "Critical"])]["Revenue"].sum()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Clients", total_clients)
        col2.metric("Avg Risk Score", avg_score)
        col3.metric("High Risk Clients", high_risk)
        col4.metric("Revenue at Risk", f"₹{revenue_risk:,.0f}")

        # ✅ SCORE INTERPRETATION
        st.subheader("🧠 Portfolio Health Interpretation")

        if avg_score < 40:
            st.success("✅ Healthy portfolio with minimal attrition risk")
        elif avg_score < 55:
            st.info("⚠️ Early warning signals emerging")
        elif avg_score < 70:
            st.warning("🔶 Moderate risk – potential business leakage")
        else:
            st.error("🚨 High attrition risk – immediate action required")

        # ✅ RISK DISTRIBUTION
        st.subheader("🔴 Risk Distribution")
        st.bar_chart(df["Risk"].value_counts())

        # ✅ REVENUE DISTRIBUTION
        st.subheader("💰 Revenue by Risk")
        st.bar_chart(df.groupby("Risk")["Revenue"].sum())

# -------------------------------------------------------
# PAGE 2 - DRIVER ANALYTICS
# -------------------------------------------------------
    elif page == "Driver Analytics":

        st.subheader("📌 Key Portfolio Insights")

        high_complaints = len(df[df["Complaints"] > 5])
        low_engagement = len(df[df["Interaction_Gap"] > 60])
        wallet_loss = len(df[df["Wallet_Share"] < 0.4])
        digital_drop = len(df[df["Digital_Usage"] < 5])

        st.write(f"• {high_complaints} clients have high complaints → service gaps")
        st.write(f"• {low_engagement} clients have low engagement → relationship weakening")
        st.write(f"• {wallet_loss} clients losing wallet share → competitor gaining")
        st.write(f"• {digital_drop} clients digitally inactive → disengagement risk")

        # DRIVER CHART
        st.subheader("📉 Attrition Drivers")

        driver_df = pd.DataFrame({
            "Driver": ["Complaints", "Low Engagement", "Wallet Loss", "Digital Drop"],
            "Count": [high_complaints, low_engagement, wallet_loss, digital_drop]
        })

        st.bar_chart(driver_df.set_index("Driver"))

# -------------------------------------------------------
# PAGE 3 - RM PRIORITY
# -------------------------------------------------------
    elif page == "RM Priority View":

        st.subheader("🚨 Top Clients Requiring Action")

        priority = df.sort_values(by="Score", ascending=False).head(20)
        st.dataframe(priority)

        st.subheader("🎯 RM Action Plan")

        st.write("""
        ✅ Immediate engagement with high-risk clients  
        ✅ Address complaint-heavy customers  
        ✅ Increase RM touchpoints  
        ✅ Focus on top revenue clients  
        """)

# -------------------------------------------------------
# PAGE 4 - CLIENT VIEW
# -------------------------------------------------------
    elif page == "Client 360° View":

        st.subheader("🔍 Client Deep Dive")

        selected = st.selectbox("Select Client", df["Client_ID"])
        client = df[df["Client_ID"] == selected].iloc[0]

        col1, col2 = st.columns(2)

        with col1:
            st.write("### Client Profile")
            st.write(client)

        with col2:
            st.write("### 🧠 AI Insight Summary")

            insights = []

            if client["Transactions"] < 10:
                insights.append("Transactions declining → migration risk")
            if client["Complaints"] > 5:
                insights.append("High complaints → dissatisfaction")
            if client["Interaction_Gap"] > 60:
                insights.append("Low engagement → weak relationship")
            if client["Wallet_Share"] < 0.4:
                insights.append("Wallet share loss → competitor capture")
            if client["Digital_Usage"] < 5:
                insights.append("Digital disengagement")

            for i in insights:
                st.write("•", i)

            st.write("### 🎯 Recommended Action")

            if client["Score"] > 85:
                st.error("Immediate escalation (Senior RM + pricing)")
            elif client["Score"] > 70:
                st.warning("High priority RM intervention")
            elif client["Score"] > 55:
                st.info("Monitor and engage")
            else:
                st.success("Client stable")

else:
    st.info("Click 'Initialize AI System' to start")
