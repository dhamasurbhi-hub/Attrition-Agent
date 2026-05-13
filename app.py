import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

st.title("🧠 TradePulse AI – Client Attrition Intelligence Agent")

st.markdown("### Multi-Dimensional Attrition Monitoring System")

# -----------------------------------------------------
# LAYER 1: DATA GENERATION (Simulates source systems)
# -----------------------------------------------------
if st.button("🚀 Initialize AI Agent"):

    np.random.seed(42)
    n = 150

    df = pd.DataFrame({
        "Client_ID": range(1, n+1),
        "Transaction_Volume": np.random.randint(1, 50, n),
        "Transaction_Value": np.random.randint(5000, 50000, n),
        "Complaint_Count": np.random.randint(0, 8, n),
        "SLA_Breach": np.random.uniform(0, 0.5, n),
        "Interaction_Gap": np.random.randint(1, 120, n),
        "RM_Contact": np.random.randint(0, 10, n),
        "Wallet_Share": np.random.uniform(0.2, 1.0, n),
        "Digital_Usage": np.random.randint(0, 30, n)
    })

    st.session_state.data = df

# -----------------------------------------------------
# LAYER 2–5: FEATURE ENGINEERING + MODEL + SCORING
# -----------------------------------------------------
if "data" in st.session_state:

    df = st.session_state.data.copy()

    # Feature Engineering
    df["Engagement_Score"] = df["RM_Contact"] / (df["Interaction_Gap"] + 1)
    df["Friction_Score"] = df["Complaint_Count"] * df["SLA_Breach"]
    df["Revenue_Proxy"] = df["Transaction_Volume"] * df["Transaction_Value"]

    # Simulated AI scoring (ensemble-style logic)
    def compute_scores(row):

        # Behavioral Drift
        drift = max(0, 30 - row["Transaction_Volume"])

        # Friction
        friction = row["Friction_Score"] * 20

        # Engagement decay
        engagement = row["Interaction_Gap"] * 0.4 - row["RM_Contact"] * 2

        # Wallet erosion
        wallet = (1 - row["Wallet_Share"]) * 50

        # Digital drop
        digital = (30 - row["Digital_Usage"])

        # FINAL ATTRITION SCORE
        aps = drift + friction + engagement + wallet + digital
        aps = max(0, min(aps, 100))

        return pd.Series([aps, wallet, friction, engagement, digital])

    df[["APS", "Wallet_Leakage", "Friction", "Engagement", "Digital"]] = df.apply(compute_scores, axis=1)

    # Risk category
    def risk(score):
        if score < 35: return "Low"
        elif score < 55: return "Watch"
        elif score < 70: return "Medium"
        elif score < 85: return "High"
        else: return "Critical"

    df["Risk"] = df["APS"].apply(risk)

# -----------------------------------------------------
# LAYER 6: DASHBOARD / INTELLIGENCE LAYER
# -----------------------------------------------------
    st.subheader("📊 Portfolio Intelligence")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Clients", len(df))
    col2.metric("Avg APS", int(df["APS"].mean()))
    col3.metric("High Risk", len(df[df["Risk"].isin(["High","Critical"])]))
    col4.metric("Critical", len(df[df["Risk"]=="Critical"]))

    st.bar_chart(df["Risk"].value_counts())

# -----------------------------------------------------
# LAYER 7: RM ACTION LAYER
# -----------------------------------------------------
    st.subheader("🚨 RM Priority Queue")

    priority = df.sort_values(by="APS", ascending=False).head(10)
    st.dataframe(priority)

# -----------------------------------------------------
# LAYER 8: DRILLDOWN INTELLIGENCE
# -----------------------------------------------------
    st.subheader("🔍 Client Deep Dive")

    selected = st.selectbox("Select Client", df["Client_ID"])

    client = df[df["Client_ID"] == selected].iloc[0]

    st.write("### Client Profile")
    st.write(client)

    st.write("### AI Explanation (Drivers)")

    drivers = []
    if client["Transaction_Volume"] < 5:
        drivers.append("Declining transaction activity")
    if client["Complaint_Count"] > 3:
        drivers.append("High complaints / service friction")
    if client["Interaction_Gap"] > 60:
        drivers.append("Low RM engagement")
    if client["Wallet_Share"] < 0.4:
        drivers.append("Wallet share erosion")
    if client["Digital_Usage"] < 5:
        drivers.append("Digital disengagement")

    for d in drivers:
        st.write("•", d)

# -----------------------------------------------------
# ACTION ENGINE (CRITICAL FOR SRS)
# -----------------------------------------------------
    st.write("### 🎯 Recommended Action")

    if client["APS"] > 85:
        st.error("Immediate escalation – Pricing + Senior RM intervention")
    elif client["APS"] > 70:
        st.warning("High priority RM engagement")
    elif client["APS"] > 55:
        st.info("Monitor & proactive outreach")
    else:
        st.success("Healthy client")
