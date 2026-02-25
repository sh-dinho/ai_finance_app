import streamlit as st

st.title("Raw FIS Output (Debug)")

if "fis_result" not in st.session_state:
    st.warning("No FIS report found. Go to Home to initialize.")
    st.stop()

st.json(st.session_state["fis_result"])