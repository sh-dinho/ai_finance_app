import streamlit as st
import pandas as pd

st.title("📂 Data Input & Raw Snapshot")

if "fis_result" not in st.session_state:
    st.warning("Please initialize data on the Home page.")
    st.stop()

bundle = st.session_state["bundle"] # If you stored it in Home.py

tab1, tab2 = st.tabs(["Daily Transactions", "Monthly Summary"])

with tab1:
    st.dataframe(bundle.df_daily, use_container_width=True)

with tab2:
    # Convert MonthlyLogEntry dataclasses to a DataFrame for viewing
    monthly_df = pd.DataFrame([vars(e) for e in bundle.entries])
    st.table(monthly_df)