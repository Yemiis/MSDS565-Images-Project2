"""UI wiring test with a synthetic upload/result fixture; real inference is checked separately."""
import sys
from pathlib import Path
from io import BytesIO
import numpy as np
from PIL import Image
import streamlit as st
from streamlit.testing.v1 import AppTest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'app'))
import deployment_utils
import project_utils


def test_upload_button_renders_every_model_and_maps(monkeypatch):
    payload=BytesIO();Image.new('RGB',(320,180),(180,70,20)).save(payload,format='PNG')
    upload=BytesIO(payload.getvalue())
    monkeypatch.setattr(st,'file_uploader',lambda *a,**kw:upload)
    monkeypatch.setattr(project_utils,'join_model',lambda *a,**kw:(object(),None))
    def fixture_explanation(model,raw,xai):
        return {'probabilities':np.array([.2,.7,.1]),'predicted':1,
                'overlays':[raw,raw,raw],'entropy':.7,'seconds':.01}
    monkeypatch.setattr(deployment_utils,'explain_one',fixture_explanation)
    app=AppTest.from_file(str(ROOT/'app/P2_Images-5_App_Project2.py')).run(timeout=60)
    assert not app.exception
    app.button[0].click().run(timeout=60)
    assert not app.exception and not app.error
    headings=[x.value for x in app.subheader]
    assert all(n in headings for n in ['mobilenetv2','resnet50','efficientnetv2m'])
    assert len(app.metric)==3
    assert len(app.get('selectbox'))==0
    assert app.session_state['result_key']
    assert len(app.session_state['results'])==3
    # A normal rerun keeps results visible without repeating the expensive backend.
    app.run(timeout=30)
    assert not app.exception and len(app.metric)==3
