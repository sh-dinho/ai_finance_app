import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import streamlit as st
from modules.mock_data import generate_mock_data
from modules.pipeline import run_fis_pipeline

st.set_page_config(page_title="Financial Intelligence System", layout="wide")

st.title("Financial Intelligence System")
st.write("A unified view of your financial health, habits, trends, and goals.")

if "bundle" not in st.session_state or "fis_result" not in st.session_state:
    st.info("Using mock data for now. Go to **Data_entry** later to plug in real data.")
    bundle = generate_mock_data()
    st.session_state["bundle"] = bundle
    st.session_state["fis_result"] = run_fis_pipeline(bundle)

fis_result = st.session_state["fis_result"]
report = fis_result["fis_report"]
score = report["intelligence_score"]["score"]
status = report["intelligence_score"]["status"]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Financial Intelligence Score", score, status)
with col2:
    st.metric("Financial Health Score", report["intelligence_score"]["financial_health_score"])
with col3:
    st.metric("Discipline Risk", report["discipline_risk"]["risk_level"])

st.subheader("Key Recommendations")
for rec in fis_result["recommendations"]:
    st.markdown(f"- {rec}")