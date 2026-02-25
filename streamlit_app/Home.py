import sys
import os
import streamlit as st

# 1. Setup Pathing (Ensures Streamlit sees the 'modules' folder)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# 2. Imports
from mock_data.generator import generate_mock_persona
from modules.pipeline import run_fis_pipeline
from modules.report_card import build_financial_report_card, summarize_financial_life
from modules.visuals import radar_chart_subscores
from modules.models import FinancialDataBundle

# 3. Page Configuration
st.set_page_config(
    page_title="Financial Intelligence System",
    page_icon="💰",
    layout="wide"
)

st.title("Financial Intelligence System")
st.write("A unified view of your financial health, habits, trends, and goals.")

# 4. Data Initialization (Mock Data)
if "bundle" not in st.session_state or "fis_result" not in st.session_state:
    with st.spinner("Initializing financial engine..."):
        # We use 'stable_salaried' as the default starter persona
        data_raw = generate_mock_persona("stable_salaried")

        # Wrap the raw dictionary into the typed FinancialDataBundle
        bundle = FinancialDataBundle(
            snapshot=data_raw["snapshot"],
            entries=data_raw["entries"],
            df_daily=data_raw["df_daily"],
            goals=data_raw["goals"],
            current_goal_values=data_raw["current_goal_values"],
            age=data_raw.get("age", 30),
            monthly_savings=data_raw.get("monthly_savings", 0.0)
        )

        st.session_state["bundle"] = bundle
        st.session_state["fis_result"] = run_fis_pipeline(bundle)

# 5. Extract Data for UI
fis_result = st.session_state["fis_result"]
report = fis_result["fis_report"]
intel = report["intelligence_score"]

# 6. Top Level Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        label="FIS Score",
        value=intel["score"],
        delta=intel["status"]
    )
with col2:
    st.metric(
        label="Health Score",
        value=intel["financial_health_score"]
    )
with col3:
    st.metric(
        label="Discipline Risk",
        value=report["discipline_risk"]["risk_level"]
    )

st.divider()

# 7. Financial Report Card Section
st.subheader("Financial Report Card")

# Generate the logic for the grade and the text summary
report_card = build_financial_report_card(intel)
summary_text = summarize_financial_life(
    intel,
    report["discipline_risk"],
    report["income_insights"],
    report["emergency_fund"],
    report["goal_insights"]
)

card_col, chart_col = st.columns([1, 1])

with card_col:
    # Big Grade Display
    st.markdown(f"""
    <div style="text-align: center; border: 2px solid #f0f2f6; border-radius: 10px; padding: 20px;">
        <h1 style="font-size: 80px; margin: 0; color: #1E88E5;">{report_card['grade']}</h1>
        <p style="font-size: 20px; color: gray;">Overall Grade</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("### Executive Summary")
    st.info(summary_text)

with chart_col:
    # Radar Chart of Sub-factors
    fig = radar_chart_subscores(report_card["subscores"])
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# 8. Actionable Recommendations
st.subheader("Key Recommendations")
recs = fis_result.get("recommendations", [])
if recs:
    for r in recs:
        st.markdown(f"✅ {r}")
else:
    st.write("No urgent recommendations at this time.")

# 9. Deep Dive Expanders
with st.expander("View Raw Intelligence Metadata"):
    st.json(report)