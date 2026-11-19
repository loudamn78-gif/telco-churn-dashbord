import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Telco Churn Dashboard", layout="wide")
st.title("Telco Customer Churn Dashboard")

df = pd.read_csv("telco_clean.csv")

st.sidebar.header("Filters")
contract_sel = st.sidebar.multiselect(
    "Contract",
    options=df["Contract"].unique(),
    default=df["Contract"].unique(),
)
tenure_sel = st.sidebar.multiselect(
    "Tenure Group",
    options=df["tenure_group"].dropna().unique(),
    default=df["tenure_group"].dropna().unique(),
)
internet_sel = st.sidebar.multiselect(
    "Internet Service",
    options=df["InternetService"].unique(),
    default=df["InternetService"].unique(),
)

filtered_df = df[
    df["Contract"].isin(contract_sel)
    & df["tenure_group"].isin(tenure_sel)
    & df["InternetService"].isin(internet_sel)
]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", len(filtered_df))
churn_rate = (filtered_df["Churn"] == "Yes").mean() * 100
col2.metric("Churn Rate (%)", f"{churn_rate:.1f}%")
col3.metric("Avg Monthly Charges", f"${filtered_df['MonthlyCharges'].mean():.2f}")
col4.metric("Avg Total Charges", f"${filtered_df['TotalCharges'].mean():.2f}")


st.divider()
col_a, col_b = st.columns(2)

with col_a:
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    sns.countplot(data=filtered_df, x="Contract", hue="Churn", ax=ax1)
    ax1.set_title("Churn by Contract")
    st.pyplot(fig1)

with col_b:
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.countplot(data=filtered_df, x="tenure_group", hue="Churn", ax=ax2)
    ax2.set_title("Churn by Tenure Group")
    st.pyplot(fig2) 

col_c, col_d = st.columns(2)

with col_c:
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    sns.countplot(data=filtered_df, x="InternetService", hue="Churn", ax=ax3)
    ax3.set_title("Churn by Internet Service")
    st.pyplot(fig3)

with col_d:
    fig4, ax4 = plt.subplots(figsize=(6, 4))
    sns.boxplot(data=filtered_df, x="Churn", y="MonthlyCharges", ax=ax4)
    ax4.set_title("Monthly Charges by Churn")
    st.pyplot(fig4)

st.divider()
st.subheader("Filtered Data Preview")
st.dataframe(filtered_df, use_container_width=True)

