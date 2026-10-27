"""Startup with the supplied real artifacts requires no training-data directory."""
from pathlib import Path
from streamlit.testing.v1 import AppTest
ROOT=Path(__file__).resolve().parents[1]

def test_startup_with_real_models_metadata():
    app=AppTest.from_file(str(ROOT/'app/P2_Images-5_App_Project2.py')).run(timeout=30)
    assert not app.exception and not app.error
    assert len(app.get('file_uploader'))==1
    assert app.title[0].value=='Project 2: Image Classification'
