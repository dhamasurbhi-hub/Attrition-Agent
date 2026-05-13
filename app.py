import streamlit as st

st.title("🤖 AI Attrition Prediction Agent (SRS Lite Version)")

st.write("Simulates enterprise attrition scoring using behavioral, operational & engagement signals")

# -------------------------
# INPUTS (Aligned to SRS dimensions)
# -------------------------
st.sidebar.header("Customer Signals")

# Behavioral
transactions = st.sidebar.slider("Transaction Frequency", 1, 50, 10)
value = st.sidebar.slider("Avg Transaction Value", 1000, 50000, 10000)

# Operational Friction
complaints = st.sidebar.slider("Complaint Count", 0, 10, 2)
sla_breach = st.sidebar.slider("SLA Breach Rate", 0.0, 1.0, 0.2)

# Engagement
interaction_gap = st.sidebar.slider("Days Since Last RM Interaction", 1, 120, 30)
rm_contacts = st.sidebar.slider("RM Contact Frequency", 0, 10, 3)

# Financial
wallet_share = st.sidebar.slider("Wallet Share", 0.1, 1.0, 0.6)

# Digital
login_freq = st.sidebar.slider("Login Frequency", 0, 30, 10)

# -------------------------
# FEATURE ENGINEERING (SRS layer)
# -------------------------
engagement_score = rm_contacts / (interaction_gap + 1)
friction_score = complaints * sla_breach
value_score = transactions * value

# -------------------------
# MULTI-DIMENSION SCORING
# -------------------------
# Behavioral decline
behavior_score = 0
if transactions < 5:
    behavior_score += 20
if value < 10000:
    behavior_score += 15

# Operational friction
friction_component = friction_score * 10

# Engagement decay
engagement_component = (interaction_gap * 0.4) - (rm_contacts * 2)

# Financial leakage
wallet_component = (1 - wallet_share) * 40

# Digital disengagement
digital_component = (20 - login_freq)

# FINAL SCORE
score = int(
    behavior_score +
    friction_component +
    engagement_component +
    wallet_component +
    digital_component
)

score = max(0, min(score, 100))  # Clamp

# -------------------------
# OUTPUT SCORE
# -------------------------
st.subheader("📊 Attrition Score")
st.metric("Score (0–100)", score)

# -------------------------
# RISK CATEGORY
# -------------------------
if score < 35:
    st.success("✅ Low Risk")
elif score < 55:
    st.info("👀 Watch")
elif score < 70:
    st.warning("⚠️ Medium Risk")
elif score < 85:
    st.error("🔥 High Risk")
else:
    st.error("🚨 Critical Risk")

# -------------------------
# DRIVERS (SRS Explainability)
# -------------------------
st.subheader("🔍 Key Risk Drivers")

drivers = []
if transactions < 5:
    drivers.append("Declining transaction activity")
if complaints > 3:
    drivers.append("High complaints")
if sla_breach > 0.3:
    drivers.append("Operational delays")
if interaction_gap > 60:
    drivers.append("Low engagement")
if wallet_share < 0.4:
    drivers.append("Wallet share erosion")
if login_freq < 5:
    drivers.append("Digital disengagement")

if drivers:
    for d in drivers:
        st.write(f"- {d}")
else:
    st.write("No major attrition signals detected")

# -------------------------
# ACTION ENGINE (Matches SRS)
