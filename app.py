import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import plotly.express as px
import shap

st.set_page_config(layout="wide")

st.title("🏦 TradePulse AI - Enterprise Attrition Intelligence")
st.caption("Real-Time Monitoring | Explainable AI | Decision Engine")

# ======================================================
# DATA GENERATION (SIMULATED LIVE SYSTEM)
# ======================================================
np.random.seed(42)
n = 800

df = pd.DataFrame({
    "Client_ID": range(10001, 10001+n),
    "Jan": np.random.randint(100, 250, n),
    "Feb": np.random.randint(80, 220, n),
    "Mar": np.random.randint(60, 180, n),
    "Apr": np.random.randint(30, 150, n),
    "Complaints": np.random.randint(0, 10, n),
    "Wallet_Share": np.random.uniform(0.1, 1, n),
    "Interaction_Days": np.random.randint(1, 120, n),
    "Revenue": np.random.randint(50000, 5000000, n)
})

# Trend
df["Trend"] = df["Apr"] - df["Jan"]

# Target (simulated churn)
df["Churn"] = (
    (df["Trend"] < -40) |
    (df["Wallet_Share"] < 0.4) |
    (df["Complaints"] > 5)
).astype(int)

# ======================================================
# MODEL
# ======================================================
features = ["Jan","Feb","Mar","Apr","Complaints","Wallet_Share","Interaction_Days"]

model = RandomForestClassifier()
model.fit(df[features], df["Churn"])

df["Score"] = (model.predict_proba(df[features])[:,1]*100).astype(int)

def risk(x):
    if x < 35: return "Low"
    elif x < 55: return "Watch"
    elif x < 70: return "Medium"
    elif x < 85: return "High"
    else: return "Critical"

df["Risk"] = df["Score"].apply(risk)

# ======================================================
# KPI CARDS
# ======================================================
st.subheader("📊 Enterprise Dashboard")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Clients", len(df))
c2.metric("Avg Score", int(df["Score"].mean()))
c3.metric("High Risk", len(df[df["Risk"].isin(["High","Critical"])]))
c4.metric("Revenue Risk", f"₹{df[df['Risk'].isin(['High','Critical'])]['Revenue'].sum():,.0f}")

# ======================================================
# 1. ALERT NOTIFICATIONS (REAL UI)
# ======================================================
st.subheader("🚨 Live Alerts")

alerts = df[df["Risk"].isin(["High","Critical"])].sort_values(by="Score", ascending=False).head(5)

for _, row in alerts.iterrows():
    st.toast(f"Client {row['Client_ID']} triggered ATTRITION ALERT | Score: {row['Score']}")

# ======================================================
# 2. CLIENT LIFECYCLE VISUALIZATION
# ======================================================
st.subheader("🔄 Client Lifecycle Flow")

lifecycle_counts = df["Risk"].value_counts().reset_index()
lifecycle_counts.columns = ["Stage","Clients"]

fig_life = px.bar(
    lifecycle_counts,
    x="Stage",
    y="Clients",
    color="Stage",
    title="Client Movement Across Lifecycle Stages"
)

st.plotly_chart(fig_life, use_container_width=True)

# ======================================================
# 3. TIME-SERIES (PORTFOLIO LEVEL)
# ======================================================
st.subheader("📈 Portfolio Trend")

avg_trend = [df["Jan"].mean(), df["Feb"].mean(), df["Mar"].mean(), df["Apr"].mean()]

fig_trend = px.line(
    x=["Jan","Feb","Mar","Apr"],
    y=avg_trend,
    markers=True,
    title="Transaction Decline Trend"
)

st.plotly_chart(fig_trend, use_container_width=True)

# ======================================================
# 4. REVENUE LOSS PREDICTION
# ======================================================
st.subheader("💰 Predicted Revenue Loss")

df["Predicted_Loss"] = df["Score"]/100 * df["Revenue"]

total_loss = df["Predicted_Loss"].sum()

st.metric("Projected Revenue Loss", f"₹{total_loss:,.0f}")

fig_loss = px.histogram(df, x="Predicted_Loss", title="Revenue Risk Distribution")
st.plotly_chart(fig_loss, use_container_width=True)

# ======================================================
# 5. SHAP EXPLAINABILITY
# ======================================================
st.subheader("🧠 AI Explainability")

explainer = shap.TreeExplainer(model)
sample = df[features].iloc[:100]

shap_values = explainer.shap_values(sample)

fig_shap = px.bar(
    x=features,
    y=np.abs(shap_values[1]).mean(axis=0),
    title="Top Drivers of Attrition"
)

st.plotly_chart(fig_shap)

# ======================================================
# 6. CLIENT DEEP DIVE
# ======================================================
st.subheader("🔍 Client 360")

client_id = st.selectbox("Select Client", df["Client_ID"])
client = df[df["Client_ID"] == client_id].iloc[0]

colA, colB = st.columns(2)

with colA:
    st.write(client)

with colB:
    st.write("### 📈 Client Trend")

    fig_client = px.line(
        x=["Jan","Feb","Mar","Apr"],
        y=[client["Jan"],client["Feb"],client["Mar"],client["Apr"]],
        markers=True
    )
    st.plotly_chart(fig_client)

    st.write("### 🧠 Insights")

    if client["Trend"] < -40:
        st.write("• Strong downward trend")
    if client["Wallet_Share"] < 0.4:
        st.write("• Wallet loss")
    if client["Complaints"] > 5:
        st.write("• High dissatisfaction")

    st.write("### 🎯 Action")
    st.warning("Immediate RM engagement required")

