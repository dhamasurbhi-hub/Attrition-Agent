import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(layout="wide")

st.title("🏦 TradePulse AI – Enterprise Attrition Intelligence System")

# =============================================================
# ✅ SESSION STATE FOR NAVIGATION
# =============================================================
if "view" not in st.session_state:
    st.session_state.view = "overview"

# =============================================================
# ✅ MULTI-SYSTEM DATA (SRS LEVEL)
# =============================================================
@st.cache_data
def generate_data():

    np.random.seed(42)
    n = 1200

    df = pd.DataFrame({
        "Client_ID": range(10001, 10001+n),

        # 🔵 Trade Products
        "LC_Volume": np.random.randint(50, 200, n),
        "BG_Volume": np.random.randint(20, 150, n),
        "Trade_Decline": np.random.randint(-80, 50, n),

        # 🟢 Treasury
        "FX_Conversion": np.random.uniform(0.2, 1, n),
        "FX_Deals": np.random.randint(5, 100, n),
        "Wallet_Share": np.random.uniform(0.1, 1, n),

        # 🟡 Lending
        "Utilization": np.random.uniform(0.1, 1, n),

        # 🔴 CRM
        "RM_Contacts": np.random.randint(0, 10, n),
        "Interaction_Days": np.random.randint(1, 120, n),

        # ⚙️ Operations
        "Complaints": np.random.randint(0, 10, n),
        "SLA_Breach": np.random.uniform(0, 1, n),

        # 🟣 Digital
        "Digital_Usage": np.random.randint(0, 50, n),

        # 💰 Revenue
        "Revenue": np.random.randint(100000, 5000000, n)
    })

    # ======================================================
    # TARGET (ATTRITION PATTERN)
    # ======================================================
    df["Churn"] = (
        (df["Trade_Decline"] < -40) |
        (df["Wallet_Share"] < 0.4) |
        (df["Complaints"] > 5) |
        (df["Interaction_Days"] > 60) |
        (df["FX_Conversion"] < 0.4)
    ).astype(int)

    return df

df = generate_data()

# =============================================================
# ✅ MODEL
# =============================================================
features = [
    "LC_Volume","BG_Volume","Trade_Decline",
    "FX_Conversion","FX_Deals","Wallet_Share",
    "Utilization","RM_Contacts","Interaction_Days",
    "Complaints","SLA_Breach","Digital_Usage"
]

model = RandomForestClassifier(n_estimators=100)
model.fit(df[features], df["Churn"])

df["Score"] = (model.predict_proba(df[features])[:,1] * 100).astype(int)

def risk(x):
    if x < 35: return "Low"
    elif x < 55: return "Watch"
    elif x < 70: return "Medium"
    elif x < 85: return "High"
    else: return "Critical"

df["Risk"] = df["Score"].apply(risk)

# =============================================================
# ✅ SIGNAL FLAGS (VERY IMPORTANT)
# =============================================================
df["Trade_Flag"] = df["Trade_Decline"] < -40
df["FX_Flag"] = df["FX_Conversion"] < 0.4
df["Wallet_Flag"] = df["Wallet_Share"] < 0.4
df["Engagement_Flag"] = df["Interaction_Days"] > 60
df["Complaint_Flag"] = df["Complaints"] > 5
df["Digital_Flag"] = df["Digital_Usage"] < 10

# =============================================================
# ✅ BUTTON CONTROL PANEL (MAIN APP NAVIGATION)
# =============================================================

st.subheader("📌 Control Panel")

col1, col2, col3, col4 = st.columns(4)

if col1.button("📊 Portfolio Overview"):
    st.session_state.view = "overview"

if col2.button("📦 Product Analysis"):
    st.session_state.view = "products"

if col3.button("🚨 Alerts"):
    st.session_state.view = "alerts"

if col4.button("👨‍💼 RM View"):
    st.session_state.view = "rm"

if st.button("🔍 Client Deep Dive"):
    st.session_state.view = "client"

# =============================================================
# 📊 VIEW 1: OVERVIEW
# =============================================================
if st.session_state.view == "overview":

    st.subheader("Portfolio Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Avg Score", int(df["Score"].mean()))
    col2.metric("High Risk", len(df[df["Risk"].isin(["High","Critical"])]))
    col3.metric("Revenue Risk", f"₹{df[df['Risk'].isin(['High','Critical'])]['Revenue'].sum():,.0f}")

    st.write("### Key Signals")

    st.write(f"• Trade decline: {df['Trade_Flag'].sum()} clients")
    st.write(f"• FX leakage: {df['FX_Flag'].sum()} clients")
    st.write(f"• Wallet loss: {df['Wallet_Flag'].sum()} clients")
    st.write(f"• Engagement gap: {df['Engagement_Flag'].sum()} clients")

# =============================================================
# 📦 VIEW 2: PRODUCT LEVEL
# =============================================================
elif st.session_state.view == "products":

    st.subheader("Product-Level Risk")

    st.dataframe(df[[
        "Client_ID",
        "LC_Volume","BG_Volume",
        "FX_Deals","FX_Conversion",
        "Utilization",
        "Score","Risk"
    ]])

# =============================================================
# 🚨 VIEW 3: ALERTS
# =============================================================
elif st.session_state.view == "alerts":

    st.subheader("High Risk Alerts")

    alerts = df[df["Risk"].isin(["High","Critical"])].sort_values(by="Score", ascending=False)

    st.dataframe(alerts.head(20))

# =============================================================
# 👨‍💼 VIEW 4: RM
# =============================================================
elif st.session_state.view == "rm":

    st.subheader("RM Action Table")

    df["RM_Status"] = np.random.choice(["Pending","Contacted","Resolved"], len(df))

    st.dataframe(df[[
        "Client_ID","Score","Risk",
        "RM_Status","Revenue"
    ]].sort_values(by="Score", ascending=False))

# =============================================================
# 🔍 VIEW 5: CLIENT
# =============================================================
elif st.session_state.view == "client":

    client_id = st.selectbox("Select Client", df["Client_ID"])
    client = df[df["Client_ID"] == client_id].iloc[0]

    st.write(client)

    st.subheader("Active Signals")

    if client["Trade_Flag"]:
        st.error("Trade decline detected")

    if client["FX_Flag"]:
        st.error("FX leakage")

    if client["Wallet_Flag"]:
        st.error("Wallet loss")

    if client["Engagement_Flag"]:
        st.warning("Low engagement")

    if client["Complaint_Flag"]:
        st.warning("High complaints")

    st.subheader("Recommended Action")

    if client["Risk"] == "Critical":
        st.error("Immediate escalation")
    elif client["Risk"] == "High":
        st.warning("RM intervention needed")
    else:
        st.success("Monitoring")
