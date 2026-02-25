from streamlit.testing.v1 import AppTest

def test_home_page_loads():
    at = AppTest.from_file("Home.py").run()
    # Check if the title is correct
    assert at.title[0].value == "Financial Intelligence System"
    # Check if the metrics are rendered
    assert len(at.metric) > 0
    # Ensure no exceptions were raised during the run
    assert not at.exception