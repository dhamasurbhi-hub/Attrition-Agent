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
# INIT DATA
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
        "Revenue": np.random.randint(50000, 5000000, n)
    })

    # Simulated Real Behavior
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

    # MODEL
    features = [
        "Transactions","Transaction_Value","Complaints",
        "SLA_Breach","Interaction_Gap","RM_Contacts",
        "Wallet_Share","Digital_Usage","Product_Usage"
    ]

    model = RandomForestClassifier(n_estimators=120)
    model.fit(df[features], df["Churn_Flag"])

    df["Probability"] = model.predict_proba(df[features])[:,1]
    df["Score"] = (df["Probability"] * 100).astype(int)

    def risk(score):
        if score < 35: return "Low"
        elif score < 55: return "Watch"
        elif score < 70: return "Medium"
        elif score < 85: return "High"
        else: return "Critical"

    df["Risk"] = df["Score"].apply(risk)

# -------------------------------------------------------
# NAVIGATION
# -------------------------------------------------------
    page = st.sidebar.radio("🔍 Navigation", [
        "Executive Overview",
        "Risk Analytics",
        "RM Priority View",
        "Client 360° View"
    ])

# -------------------------------------------------------
# EXECUTIVE VIEW
# -------------------------------------------------------
    if page == "Executive Overview":

        st.subheader("📊 Portfolio Overview")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Clients", len(df))
        col2.metric("Avg Risk Score", int(df["Score"].mean()))
        col3.metric("High Risk Clients", len(df[df["Risk"].isin(["High","Critical"])]))
        col4.metric("Revenue at Risk", f"₹{df[df['Risk'].isin(['High','Critical'])]['Revenue'].sum():,.0f}")

        st.markdown("### 🔴 Risk Distribution")
        st.bar_chart(df["Risk"].value_counts())

        st.markdown("### 💰 Revenue Risk Analysis")
        st.bar_chart(df.groupby("Risk")["Revenue"].sum())

# -------------------------------------------------------
# RISK ANALYTICS
# -------------------------------------------------------
    elif page == "Risk Analytics":

        st.subheader("📈 Behavior Insights")

        st.line_chart(df.sort_values("Client_ID")["Transactions"])

        st.subheader("⚠️ Key Risk Indicators")

        col1, col2 = st.columns(2)

        with col1:
            st.write("High Complaints Clients:",
                     len(df[df["Complaints"] > 5]))

            st.write("Low Engagement Clients:",
                     len(df[df["Interaction_Gap"] > 60]))

        with col2:
            st.write("Low Wallet Share:",
                     len(df[df["Wallet_Share"] < 0.4]))

            st.write("Digital Drop-off:",
                     len(df[df["Digital_Usage"] < 5]))

# -------------------------------------------------------
# RM PRIORITY VIEW
# -------------------------------------------------------
    elif page == "RM Priority View":

        st.subheader("🚨 Top Clients to Act On")

        priority = df.sort_values(by="Score", ascending=False).head(15)

        st.dataframe(priority)

        st.markdown("### 🎯 Suggested RM Strategy")

        st.write("""
        • Immediate outreach to top 10 risky clients  
        • Pricing review for wallet share loss  
        • Digital onboarding for low engagement  
        """)

# -------------------------------------------------------
# CLIENT 360 VIEW
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
            st.write("### AI Explanation")

            insights = []

            if client["Transactions"] < 10:
                insights.append("Transaction activity is dropping → migration risk")

            if client["Complaints"] > 5:
                insights.append("High complaints → dissatisfaction")

            if client["Interaction_Gap"] > 60:
                insights.append("Low RM engagement")

            if client["Wallet_Share"] < 0.4:
                insights.append("Wallet share erosion → competitor gaining")

            if client["Digital_Usage"] < 5:
                insights.append("Digital disengagement")

            for i in insights:
                st.write("•", i)

            st.write("### 🎯 Action Recommendation")

            if client["Score"] > 85:
                st.error("Immediate escalation needed")
            elif client["Score"] > 70:
                st.warning("High priority RM intervention")
            elif client["Score"] > 55:
                st.info("Monitor closely")
            else:
                st.success("Client stable")

else:
    st.info("Click 'Initialize System' to load AI model")
