import streamlit as pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(layout="wide")

st.title("🏦 TradePulse AI – Attrition Intelligence Platform")
st.caption("Data-Driven Monitoring | Signal-Based Decision Engine")

# =====================================================
# ✅ DATA GENERATION (MULTI-SYSTEM, NO HEAVY CHARTS)
# =====================================================
@st.cache_data
def generate_data():

    np.random.seed(42)
    n = 800

    df = pd.DataFrame({
        "Client_ID": range(10001, 10001+n),

        # Trade
        "LC_Volume": np.random.randint(20, 200, n),
        "Trade_Decline": np.random.randint(-80, 40, n),

        # Treasury
        "Wallet_Share": np.random.uniform(0.1, 1, n),

        # CRM
        "RM_Contacts": np.random.randint(0, 10, n),
        "Interaction_Days": np.random.randint(1, 120, n),

        # Operations
        "Complaints": np.random.randint(0, 10, n),
        "SLA_Breach": np.random.uniform(0, 1, n),

        # Digital
        "Digital_Usage": np.random.randint(0, 50, n),

        # Revenue
        "Revenue": np.random.randint(50000, 5000000, n)
    })

    # TARGET (simulated)
    df["Churn"] = (
        (df["Trade_Decline"] < -40) |
        (df["Wallet_Share"] < 0.4) |
        (df["Complaints"] > 5) |
        (df["Interaction_Days"] > 60)
    ).astype(int)

    # RM Status
    df["RM_Status"] = np.random.choice(
        ["Pending", "Contacted", "Resolved"], size=n
    )

    return df

df = generate_data()

# =====================================================
# ✅ MODEL
# =====================================================
features = [
    "LC_Volume","Trade_Decline","Wallet_Share",
    "RM_Contacts","Interaction_Days",
    "Complaints","SLA_Breach","Digital_Usage"
]

model = RandomForestClassifier(n_estimators=100)
model.fit(df[features], df["Churn"])

df["Attrition_Score"] = (model.predict_proba(df[features])[:,1] * 100).astype(int)

# =====================================================
# ✅ RISK SEGMENT
# =====================================================
def risk(x):
    if x < 35: return "Low"
    elif x < 55: return "Watch"
    elif x < 70: return "Medium"
    elif x < 85: return "High"
    else: return "Critical"

df["Risk"] = df["Attrition_Score"].apply(risk)

# =====================================================
# ✅ CREATE SIGNAL FLAGS (MOST IMPORTANT)
# =====================================================
df["Trade_Flag"] = df["Trade_Decline"] < -40
df["Wallet_Flag"] = df["Wallet_Share"] < 0.4
df["Engagement_Flag"] = df["Interaction_Days"] > 60
df["Complaint_Flag"] = df["Complaints"] > 5
df["Digital_Flag"] = df["Digital_Usage"] < 10

# =====================================================
# ✅ NAVIGATION
# =====================================================
page = st.sidebar.radio("Navigation", [
    "📊 Executive Summary",
    "📋 Client Signals Table",
    "🚨 Alerts & Priority",
    "👨‍💼 RM Workflow",
    "🔍 Client Deep Dive"
])

# =====================================================
# 📊 EXECUTIVE SUMMARY
# =====================================================
if page == "📊 Executive Summary":

    st.subheader("Portfolio Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Avg Score", int(df["Attrition_Score"].mean()))
    col2.metric("High Risk Clients", len(df[df["Risk"].isin(["High","Critical"])]))
    col3.metric("Revenue at Risk", f"₹{df[df['Risk'].isin(['High','Critical'])]['Revenue'].sum():,.0f}")

    st.write("### Key Insights")

    st.write(f"• {len(df[df['Trade_Flag']])} clients show trade decline")
    st.write(f"• {len(df[df['Wallet_Flag']])} clients losing wallet share")
    st.write(f"• {len(df[df['Complaint_Flag']])} clients have complaints")
    st.write(f"• {len(df[df['Engagement_Flag']])} clients disengaged")

# =====================================================
# 📋 CLIENT SIGNAL TABLE (CORE OF SYSTEM)
# =====================================================
elif page == "📋 Client Signals Table":

    st.subheader("Client Risk Signals")

    st.dataframe(df[[
        "Client_ID","Attrition_Score","Risk",
        "Trade_Flag","Wallet_Flag","Engagement_Flag",
        "Complaint_Flag","Digital_Flag","Revenue"
    ]])

# =====================================================
# 🚨 ALERTS
# =====================================================
elif page == "🚨 Alerts & Priority":

    st.subheader("High Priority Alerts")

    alerts = df[df["Risk"].isin(["High","Critical"])].sort_values(by="Attrition_Score", ascending=False)

    st.dataframe(alerts.head(20))

# =====================================================
# 👨‍💼 RM WORKFLOW
# =====================================================
elif page == "👨‍💼 RM Workflow":

    st.subheader("RM Action Table")

    st.dataframe(df[[
        "Client_ID","Risk","Attrition_Score",
        "RM_Status","Revenue"
    ]].sort_values(by="Attrition_Score", ascending=False))

# =====================================================
# 🔍 CLIENT VIEW
# =====================================================
elif page == "🔍 Client Deep Dive":

    st.subheader("Client Analysis")

    client_id = st.selectbox("Select Client", df["Client_ID"])
    client = df[df["Client_ID"] == client_id].iloc[0]

    st.write(client)

    st.subheader("Active Risk Signals")

    if client["Trade_Flag"]:
        st.write("• Trade decline detected")

    if client["Wallet_Flag"]:
        st.write("• Wallet share loss")

    if client["Complaint_Flag"]:
        st.write("• High complaints")

    if client["Engagement_Flag"]:
        st.write("• Low engagement")

    if client["Digital_Flag"]:
        st.write("• Digital inactivity")

    st.subheader("Recommended Action")

    if client["Risk"] == "Critical":
        st.error("Immediate escalation")
    elif client["Risk"] == "High":
        st.warning("RM intervention required")
    else:
        st.info("Monitoring")
