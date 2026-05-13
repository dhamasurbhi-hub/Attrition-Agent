import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")
st.title("🤖 AI Customer Attrition Agent (Full Demo App)")

st.markdown("### Interactive Portfolio Dashboard with AI Scoring Engine")

# -------------------------------------------------
# BUTTON: GENERATE DATA
# -------------------------------------------------
if "data" not in st.session_state:

    st.session_state.data = None

if st.button("🔄 Generate Dummy Data"):

    np.random.seed(42)
    n = 100

    data = pd.DataFrame({
        "Customer_ID": range(1, n+1),
        "Transactions": np.random.randint(1, 50, n),
        "Avg_Value": np.random.randint(5000, 50000, n),
        "Complaints": np.random.randint(0, 8, n),
        "SLA_Breach": np.random.uniform(0, 0.5, n),
        "Interaction_Days": np.random.randint(1, 120, n),
        "RM_Contacts": np.random.randint(0, 10, n),
        "Wallet_Share": np.round(np.random.uniform(0.2, 1.0, n), 2),
        "Login_Freq": np.random.randint(0, 30, n)
    })

    # -------------------------
    # SCORING FUNCTION
    # -------------------------
    def calculate_score(row):
        score = 0
        
        if row["Transactions"] < 5:
            score += 20
        if row["Avg_Value"] < 10000:
            score += 15

        score += row["Complaints"] * row["SLA_Breach"] * 10
        score += (row["Interaction_Days"] * 0.4) - (row["RM_Contacts"] * 2)
        score += (1 - row["Wallet_Share"]) * 40
        score += (20 - row["Login_Freq"])

        return int(max(0, min(score, 100)))

    data["Churn_Score"] = data.apply(calculate_score, axis=1)

    def risk(score):
        if score < 35: return "Low"
        elif score < 55: return "Watch"
        elif score < 70: return "Medium"
        elif score < 85: return "High"
        else: return "Critical"

    data["Risk"] = data["Churn_Score"].apply(risk)

    st.session_state.data = data

# -------------------------------------------------
# IF DATA EXISTS
# -------------------------------------------------
if st.session_state.data is not None:

    data = st.session_state.data

    # -------------------------------------------------
    # BUTTON: REFRESH
    # -------------------------------------------------
    if st.button("♻️ Refresh Dashboard"):
        st.experimental_rerun()

    # -------------------------------------------------
    # FILTER OPTION
    # -------------------------------------------------
    st.sidebar.header("Filters")

    risk_filter = st.sidebar.multiselect(
        "Select Risk Level",
        options=data["Risk"].unique(),
        default=data["Risk"].unique()
    )

    filtered_data = data[data["Risk"].isin(risk_filter)]

    # -------------------------------------------------
    # METRICS
    # -------------------------------------------------
    st.subheader("📊 Portfolio Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Customers", len(filtered_data))
    col2.metric("Avg Score", int(filtered_data["Churn_Score"].mean()))
    col3.metric("High Risk", len(filtered_data[filtered_data["Risk"].isin(["High","Critical"])]))
    col4.metric("Critical", len(filtered_data[filtered_data["Risk"] == "Critical"]))

    # -------------------------------------------------
    # CHART
    # -------------------------------------------------
    st.subheader("📈 Risk Distribution")
    st.bar_chart(filtered_data["Risk"].value_counts())

    # -------------------------------------------------
    # TOP 10 CUSTOMERS BUTTON
    # -------------------------------------------------
    if st.button("🚨 Show Top 10 Risky Customers"):
        top10 = filtered_data.sort_values(by="Churn_Score", ascending=False).head(10)
        st.dataframe(top10)

    # -------------------------------------------------
    # FULL DATA TABLE
    # -------------------------------------------------
    st.subheader("📋 Customer Portfolio")
    st.dataframe(filtered_data)

    # -------------------------------------------------
    # DRILLDOWN
    # -------------------------------------------------
    st.subheader("🔍 Customer Insight")

    selected = st.selectbox("Select Customer ID", filtered_data["Customer_ID"])

    cust = filtered_data[filtered_data["Customer_ID"] == selected].iloc[0]

    colA, colB = st.columns(2)

    with colA:
        st.write("### Customer Details")
        st.write(cust)

    with colB:
        st.write("### Risk Drivers")

        drivers = []
        if cust["Transactions"] < 5:
            drivers.append("Low transactions")
        if cust["Complaints"] > 3:
            drivers.append("High complaints")
        if cust["Interaction_Days"] > 60:
            drivers.append("Low engagement")
        if cust["Wallet_Share"] < 0.4:
            drivers.append("Wallet leakage")
        if cust["Login_Freq"] < 5:
            drivers.append("Digital drop")

        if drivers:
            for d in drivers:
                st.write("•", d)
        else:
            st.write("No major issues")

        # ACTION ENGINE
        st.write("### Recommended Action")

        score = cust["Churn_Score"]

        if score > 85:
            st.error("Immediate retention action required")
        elif score > 70:
            st.warning("High priority RM intervention")
        elif score > 55:
            st.info("Monitor customer")
        else:
            st.success("Customer healthy")

# -------------------------------------------------
# DEFAULT MESSAGE
# -------------------------------------------------
else:
    st.info("Click 'Generate Dummy Data' to start the demo")

