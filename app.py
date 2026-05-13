import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(layout="wide")

st.title("🧠 TradePulse AI – Attrition Intelligence Dashboard")
st.markdown("### Predict → Explain → Act")

# -------------------------------------------------------
# BUTTONS (CORE CONTROL)
# -------------------------------------------------------
colA, colB = st.columns(2)

with colA:
    init_btn = st.button("🚀 Initialize AI System")

with colB:
    refresh_btn = st.button("♻️ Refresh Data")

# -------------------------------------------------------
# INITIALIZE DATA
# -------------------------------------------------------
if init_btn or refresh_btn:

    np.random.seed(None)  # fresh each time
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

    # Target
    df["Churn_Flag"] = (
        (df["Transactions"] < 10) &
        (df["Interaction_Gap"] > 60) |
        (df["Wallet_Share"] < 0.3) |
        (df["Complaints"] > 5)
    ).astype(int)

    st.session_state.df = df

# -------------------------------------------------------
# IF DATA EXISTS
# -------------------------------------------------------
if "df" in st.session_state:

    df = st.session_state.df.copy()

    # MODEL
    features = [
        "Transactions","Transaction_Value","Complaints","SLA_Breach",
        "Interaction_Gap","RM_Contacts","Wallet_Share",
        "Digital_Usage","Product_Usage"
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
# SIDEBAR FILTER
# -------------------------------------------------------
    st.sidebar.header("🔍 Filters")

    selected_risk = st.sidebar.multiselect(
        "Select Risk Levels",
        options=df["Risk"].unique(),
        default=df["Risk"].unique()
    )

    df = df[df["Risk"].isin(selected_risk)]

# -------------------------------------------------------
# DASHBOARD METRICS
# -------------------------------------------------------
    st.subheader("📊 Portfolio KPIs")

    avg_score = int(df["Score"].mean())
    high_risk = len(df[df["Risk"].isin(["High","Critical"])])
    revenue_risk = df[df["Risk"].isin(["High","Critical"])]["Revenue"].sum()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Clients", len(df))
    c2.metric("Avg Score", avg_score)
    c3.metric("High Risk Clients", high_risk)
    c4.metric("Revenue at Risk", f"₹{revenue_risk:,.0f}")

# -------------------------------------------------------
# SCORE INTERPRETATION
# -------------------------------------------------------
    st.subheader("🧠 Portfolio Health")

    if avg_score < 40:
        st.success("✅ Healthy portfolio")
    elif avg_score < 55:
        st.info("⚠️ Early warning stage")
    elif avg_score < 70:
        st.warning("🔶 Moderate risk")
    else:
        st.error("🚨 High attrition risk")

# -------------------------------------------------------
# GRAPH 1
# -------------------------------------------------------
    st.subheader("📉 Client Risk Distribution")

    st.write("👉 Shows how many clients fall in each risk category")

    st.bar_chart(df["Risk"].value_counts())

# -------------------------------------------------------
# GRAPH 2
# -------------------------------------------------------
    st.subheader("💰 Revenue at Risk by Segment")

    st.write("👉 Shows business exposure by risk")

    st.bar_chart(df.groupby("Risk")["Revenue"].sum())

# -------------------------------------------------------
# GRAPH 3
# -------------------------------------------------------
    st.subheader("📊 Attrition Drivers")

    high_complaints = len(df[df["Complaints"] > 5])
    low_engagement = len(df[df["Interaction_Gap"] > 60])
    wallet_loss = len(df[df["Wallet_Share"] < 0.4])
    digital_drop = len(df[df["Digital_Usage"] < 5])

    driver_df = pd.DataFrame({
        "Driver": ["Complaints", "Engagement", "Wallet Loss", "Digital Drop"],
        "Count": [high_complaints, low_engagement, wallet_loss, digital_drop]
    })

    st.bar_chart(driver_df.set_index("Driver"))

# -------------------------------------------------------
# BUTTON: TOP RISK CLIENTS
# -------------------------------------------------------
    if st.button("🚨 Show Top 10 Risk Clients"):
        top10 = df.sort_values(by="Score", ascending=False).head(10)
        st.dataframe(top10)

# -------------------------------------------------------
# CLIENT DRILLDOWN
# -------------------------------------------------------
    st.subheader("🔍 Client Deep Dive")

    selected = st.selectbox("Select Client", df["Client_ID"])

    client = df[df["Client_ID"] == selected].iloc[0]

    st.write(client)

    st.subheader("🧠 Why is this client risky?")

    if client["Transactions"] < 10:
        st.write("• Low transactions")
    if client["Complaints"] > 5:
        st.write("• High complaints")
    if client["Interaction_Gap"] > 60:
        st.write("• Low engagement")
    if client["Wallet_Share"] < 0.4:
        st.write("• Wallet share loss")

# -------------------------------------------------------
# ACTION LAYER
# -------------------------------------------------------
    st.subheader("🎯 Recommended Actions")

    st.write("""
✅ Immediate RM outreach  
✅ Resolve complaints  
✅ Improve engagement  
✅ Retain high-value clients  
""")

else:
    st.info("Click 'Initialize AI System' to start")
