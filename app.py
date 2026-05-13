import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(layout="wide")

# -------------------------------------------------------
# TITLE
# -------------------------------------------------------
st.title("🧠 TradePulse AI Agent")
st.markdown("### Customer Attrition Intelligence System")

# -------------------------------------------------------
# SRS INTRODUCTION SCREEN (CRITICAL ADD)
# -------------------------------------------------------
st.subheader("📌 AI Agent Overview")

st.markdown("""
This AI agent continuously analyzes customer behavior to predict attrition risk.

### 🧠 What the system does:
- Monitors **transaction behavior**
- Detects **service friction (complaints, delays)**
- Tracks **relationship engagement**
- Identifies **wallet share leakage**
- Measures **digital disengagement**

### 🎯 Output generated:
- Attrition Probability Score (0–100)
- Risk classification (Low → Critical)
- Key drivers of attrition
- Revenue at risk
- Recommended RM actions

👉 Click *Initialize AI System* to simulate full pipeline
""")

# -------------------------------------------------------
# BUTTONS
# -------------------------------------------------------
colA, colB = st.columns(2)

with colA:
    init_btn = st.button("🚀 Initialize AI Agent")

with colB:
    refresh_btn = st.button("♻️ Regenerate Data")

# -------------------------------------------------------
# INITIALIZE DATA + MODEL PIPELINE
# -------------------------------------------------------
if init_btn or refresh_btn:

    np.random.seed(None)
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

    # Simulated learned behavior
    df["Churn_Flag"] = (
        (df["Transactions"] < 10) &
        (df["Interaction_Gap"] > 60) |
        (df["Wallet_Share"] < 0.3) |
        (df["Complaints"] > 5)
    ).astype(int)

    st.session_state.df = df

# -------------------------------------------------------
# MAIN ENGINE (RUN ONLY AFTER INITIALIZATION)
# -------------------------------------------------------
if "df" in st.session_state:

    df = st.session_state.df.copy()

    # MODEL
    features = [
        "Transactions","Transaction_Value","Complaints",
        "SLA_Breach","Interaction_Gap","RM_Contacts",
        "Wallet_Share","Digital_Usage","Product_Usage"
    ]

    model = RandomForestClassifier(n_estimators=100)
    model.fit(df[features], df["Churn_Flag"])

    df["Score"] = (model.predict_proba(df[features])[:, 1] * 100).astype(int)

    def risk(x):
        if x < 35: return "Low"
        elif x < 55: return "Watch"
        elif x < 70: return "Medium"
        elif x < 85: return "High"
        else: return "Critical"

    df["Risk"] = df["Score"].apply(risk)

# -------------------------------------------------------
# PORTFOLIO SUMMARY
# -------------------------------------------------------
    st.subheader("📊 Portfolio Intelligence")

    avg_score = int(df["Score"].mean())
    high_risk = len(df[df["Risk"].isin(["High","Critical"])])
    revenue_risk = df[df["Risk"].isin(["High","Critical"])]["Revenue"].sum()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Clients", len(df))
    c2.metric("Attrition Score", avg_score)
    c3.metric("High Risk Clients", high_risk)
    c4.metric("Revenue at Risk", f"₹{revenue_risk:,.0f}")

# -------------------------------------------------------
# INTERPRETATION (EXPLAIN WHAT SCORE MEANS)
# -------------------------------------------------------
    st.subheader("🧠 Interpretation")

    if avg_score < 40:
        st.success("Portfolio is stable with low attrition signals")
    elif avg_score < 55:
        st.info("Early warning: some clients showing disengagement")
    elif avg_score < 70:
        st.warning("Moderate attrition risk emerging")
    else:
        st.error("High attrition risk – immediate action needed")

# -------------------------------------------------------
# DRIVER ANALYSIS
# -------------------------------------------------------
    st.subheader("📉 Why Attrition is Happening")

    high_complaints = len(df[df["Complaints"] > 5])
    low_engagement = len(df[df["Interaction_Gap"] > 60])
    wallet_loss = len(df[df["Wallet_Share"] < 0.4])
    digital_drop = len(df[df["Digital_Usage"] < 5])

    st.bar_chart(pd.DataFrame({
        "Driver": ["Complaints", "Engagement Gap", "Wallet Loss", "Digital Drop"],
        "Count": [high_complaints, low_engagement, wallet_loss, digital_drop]
    }).set_index("Driver"))

# -------------------------------------------------------
# ACTION ENGINE
# -------------------------------------------------------
    st.subheader("🎯 Recommended Actions")

    st.write("""
✅ Engage top risk clients immediately  
✅ Resolve complaints & service issues  
✅ Improve RM interaction frequency  
✅ Protect revenue-heavy accounts  
""")

# -------------------------------------------------------
# CLIENT LEVEL
# -------------------------------------------------------
    st.subheader("🔍 Client Deep Dive")

    selected = st.selectbox("Select Client", df["Client_ID"])
    client = df[df["Client_ID"] == selected].iloc[0]

    st.write(client)

    st.subheader("🧠 Key Risk Drivers")

    if client["Transactions"] < 10:
        st.write("• Declining transactions")
    if client["Complaints"] > 5:
        st.write("• High complaints")
    if client["Interaction_Gap"] > 60:
        st.write("• Low engagement")
    if client["Wallet_Share"] < 0.4:
        st.write("• Wallet leakage")

else:
    st.warning("👉 Please initialize the AI Agent to start")
