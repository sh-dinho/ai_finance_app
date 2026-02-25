import streamlit as st
from modules.mock_data import generate_mock_data
from modules.pipeline import run_fis_pipeline

st.title("Data Entry")

st.write("For now, this app uses mock data. Later, you can upload your own CSV/JSON files here.")

if st.button("Regenerate Mock Data"):
    bundle = generate_mock_data()
    st.session_state["bundle"] = bundle
    st.session_state["fis_result"] = run_fis_pipeline(bundle)
    st.success("Mock data regenerated and pipeline re-run.")

if "fis_result" in st.session_state:
    st.json(st.session_state["fis_result"]["fis_report"]["ratios"])
else:
    st.info("No data loaded yet. Go to Home to initialize mock data.")