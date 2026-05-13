import streamlit as st

st.title("AI Attrition Prediction Agent")

st.write("Enterprise-style churn scoring based on multiple signals")

# -------------------------
# INPUTS
# -------------------------
st.sidebar.header("Customer Data")

transactions = st.sidebar.slider("Transaction Frequency", 1, 50, 10)
value = st.sidebar.slider("Transaction Value", 1000, 50000, 10000)

complaints = st.sidebar.slider("Complaint Count", 0, 10, 2)
sla = st.sidebar.slider("SLA Breach Rate", 0.0, 1.0, 0.2)

interaction = st.sidebar.slider("Days Since Interaction", 1, 120, 30)
rm = st.sidebar.slider("RM Contacts", 0, 10, 3)

wallet = st.sidebar.slider("Wallet Share", 0.1, 1.0, 0.6)
login = st.sidebar.slider("Login Frequency", 0, 30, 10)

# -------------------------
# FEATURE LOGIC
# -------------------------
friction = complaints * sla
engagement = rm / (interaction + 1)

# -------------------------
# SCORING
# -------------------------
score = 0

# Behavior
if transactions < 5:
    score += 20
if value < 10000:
    score += 15

# Friction
score += friction * 10

# Engagement
score += (interaction * 0.4) - (rm * 2)

# Wallet leakage
score += (1 - wallet) * 40

# Digital
score += (20 - login)

score = int(max(0, min(score, 100)))

# -------------------------
# OUTPUT
# -------------------------
st.subheader("Churn Score")
st.metric("Score", score)

# Risk category
if score < 35:
    st.success("Low Risk")
elif score < 55:
    st.info("Watch")
elif score < 70:
    st.warning("Medium Risk")
elif score < 85:
    st.error("High Risk")
else:
    st.error("Critical Risk")

# -------------------------
# DRIVERS
# -------------------------
st.subheader("Key Drivers")

drivers = []

if transactions < 5:
    drivers.append("Low activity")
if complaints > 3:
    drivers.append("High complaints")
if interaction > 60:
    drivers.append("Low engagement")
if wallet < 0.4:
    drivers.append("Wallet loss")
if login < 5:
    drivers.append("Digital drop")

if drivers:
    for d in drivers:
        st.write("-", d)
else:
    st.write("No major risks")

# -------------------------
# ACTION
# -------------------------
st.subheader("Recommended Action")

if score > 85:
    st.write("Immediate retention action")
elif score > 70:
    st.write("RM intervention required")
elif score > 55:
    st.write("Monitor customer")
else:
    st.write("Customer healthy")

