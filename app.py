import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(layout="wide")

st.title("🧠 TradePulse AI – Attrition Intelligence Dashboard")
st.markdown("### Data → Prediction → Insight → Action")

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

    features = [
        "Transactions","Transaction_Value","Complaints",
        "SLA_Breach","Interaction_Gap","RM_Contacts",
        "Wallet_Share","Digital_Usage","Product_Usage"
    ]

    model = RandomForestClassifier(n_estimators=120)
    model.fit(df[features], df["Churn_Flag"])

    df["Probability"] = model.predict_proba(df[features])[:, 1]
    df["Score"] = (df["Probability"] * 100).astype(int)

    def risk(score):
        if score < 35: return "Low"
        elif score < 55: return "Watch"
        elif score < 70: return "Medium"
        elif score < 85: return "High"
        else: return "Critical"

    df["Risk"] = df["Score"].apply(risk)

# -------------------------------------------------------
# EXECUTIVE DASHBOARD
# -------------------------------------------------------
    st.subheader("📊 1. Portfolio Overview")

    total_clients = len(df)
    avg_score = int(df["Score"].mean())
    high_risk = len(df[df["Risk"].isin(["High","Critical"])])
    revenue_risk = df[df["Risk"].isin(["High","Critical"])]["Revenue"].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Clients", total_clients)
    col2.metric("Avg Risk Score", avg_score)
    col3.metric("High Risk Clients", high_risk)
    col4.metric("Revenue at Risk", f"₹{revenue_risk:,.0f}")

# -------------------------------------------------------
# EXPLAIN SCORE
# -------------------------------------------------------
    st.subheader("🧠 What does Average Risk Score mean?")

    if avg_score < 40:
        st.success("✅ Portfolio is Healthy")
    elif avg_score < 55:
        st.info("⚠️ Early Warning Stage")
    elif avg_score < 70:
        st.warning("🔶 Moderate Risk - leakage starting")
    else:
        st.error("🚨 High Risk - urgent intervention needed")

# -------------------------------------------------------
# GRAPH 1: RISK DISTRIBUTION
# -------------------------------------------------------
    st.subheader("📉 2. Risk Distribution")

    st.markdown("""
👉 This graph shows how many clients fall into each risk category.  
👉 Helps identify size of attrition problem.
""")

    st.bar_chart(df["Risk"].value_counts())

# -------------------------------------------------------
# GRAPH 2: REVENUE AT RISK
# -------------------------------------------------------
    st.subheader("💰 3. Revenue Exposure by Risk")

    st.markdown("""
👉 Shows how much revenue is linked to risky clients.  
👉 Helps management see financial impact.
""")

    st.bar_chart(df.groupby("Risk")["Revenue"].sum())

# -------------------------------------------------------
# GRAPH 3: DRIVER ANALYSIS
# -------------------------------------------------------
    st.subheader("📊 4. Why Customers Are Churning")

    st.markdown("""
👉 Identifies key reasons behind attrition.  
👉 Helps prioritize what needs to be fixed.
""")

    high_complaints = len(df[df["Complaints"] > 5])
    low_engagement = len(df[df["Interaction_Gap"] > 60])
    wallet_loss = len(df[df["Wallet_Share"] < 0.4])
    digital_drop = len(df[df["Digital_Usage"] < 5])

    driver_df = pd.DataFrame({
        "Driver": ["Complaints", "Low Engagement", "Wallet Loss", "Digital Drop"],
        "Count": [high_complaints, low_engagement, wallet_loss, digital_drop]
    })

    st.bar_chart(driver_df.set_index("Driver"))

# -------------------------------------------------------
# INSIGHTS PANEL
# -------------------------------------------------------
    st.subheader("📌 Key Insights")

    st.write(f"• {high_complaints} clients unhappy due to complaints")
    st.write(f"• {low_engagement} clients not contacted by RM")
    st.write(f"• {wallet_loss} clients shifting business to competitors")
    st.write(f"• {digital_drop} clients disengaging digitally")

# -------------------------------------------------------
# ACTIONS
# -------------------------------------------------------
    st.subheader("🎯 Recommended Actions")

    st.write("""
✅ Focus RM on high-risk clients  
✅ Fix complaint resolution issues  
✅ Increase relationship engagement  
✅ Retain high-value clients urgently  
""")

# -------------------------------------------------------
# CLIENT DRILLDOWN
# -------------------------------------------------------
    st.subheader("🔍 Client Deep Dive")

    selected = st.selectbox("Select Client", df["Client_ID"])
    client = df[df["Client_ID"] == selected].iloc[0]

    st.write(client)

    st.subheader("🧠 Why this client is risky?")

    if client["Transactions"] < 10:
        st.write("• Transactions declining")
    if client["Complaints"] > 5:
        st.write("• High complaints")
    if client["Interaction_Gap"] > 60:
        st.write("• Low engagement")
    if client["Wallet_Share"] < 0.4:
        st.write("• Wallet share loss")

else:
    st.info("Click 'Initialize AI System'")
