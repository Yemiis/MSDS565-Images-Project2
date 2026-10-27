"""Read-only checks of real artifacts and input boundaries; no project data created."""
import sys,shutil,tempfile,json
from pathlib import Path
from io import BytesIO
import numpy as np
import pytest
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'app'))
from deployment_utils import load_contract,prepare_upload


def test_real_saved_artifacts_and_class_order():
    metadata,geometry,mapping,names,key=load_contract(ROOT/'models')
    assert names==['ball-peen-hammer','claw-hammer','sledgehammer']
    assert metadata['tensorflow']=='2.20.0'
    assert len(key)==64


def test_corrupt_probe_is_rejected_before_inference():
    with tempfile.TemporaryDirectory() as directory:
        models=Path(directory)/'models';shutil.copytree(ROOT/'models',models)
        with (models/'P2_N3_mobilenetv2.keras').open('ab') as stream:stream.write(b'changed')
        with pytest.raises(ValueError,match='differs from Notebook 3'):
            load_contract(models)


def test_upload_preserves_raw_geometry_without_rescaling():
    _,geometry,_,_,_=load_contract(ROOT/'models')
    data=BytesIO();Image.new('RGBA',(400,100),(220,30,10,255)).save(data,format='PNG')
    original,raw=prepare_upload(data.getvalue(),geometry)
    assert original.size==(400,100)
    assert raw.dtype==np.uint8 and raw.shape==(224,224,3)
    np.testing.assert_array_equal(raw[0,0],[127,127,127])
    np.testing.assert_array_equal(raw[112,112],[220,30,10])


def test_invalid_upload_fails_cleanly():
    _,geometry,_,_,_=load_contract(ROOT/'models')
    with pytest.raises(OSError):prepare_upload(b'not an image',geometry)
