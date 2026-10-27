"""Synthetic in-memory checks only; these are not project training/evaluation data."""
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'app'))
sys.path.insert(0, str(ROOT/'notebooks'))
from project_utils import resize_rgb, read_mapping
from pipeline_utils import pixel_hash, as_bool
import pandas as pd

class GeometryChecks(unittest.TestCase):
    def test_long_subject_preserved_with_identical_padding(self):
        # A wide, solid subject must remain wide rather than stretched into a square.
        array = resize_rgb(Image.new('RGB',(400,100),(255,0,0)))
        self.assertEqual(array.shape,(224,224,3))
        self.assertEqual(array.dtype,np.uint8)
        np.testing.assert_array_equal(array[0,0],[127,127,127])
        np.testing.assert_array_equal(array[112,112],[255,0,0])
        np.testing.assert_array_equal(array[:84],np.full((84,224,3),127,dtype='uint8'))

    def test_transparency_composited_to_grey(self):
        array=resize_rgb(Image.new('RGBA',(224,224),(0,0,0,0)))
        np.testing.assert_array_equal(array,np.full((224,224,3),127,dtype='uint8'))

    def test_exact_hash_distinguishes_subject_content(self):
        left=Image.new('RGB',(224,224),(120,30,40))
        self.assertEqual(pixel_hash(left),pixel_hash(left.copy()))
        self.assertNotEqual(pixel_hash(left),pixel_hash(Image.new('RGB',(224,224),(120,30,41))))

    def test_mapping_order_and_rejection(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'mapping.json'
            path.write_text('{"b":1,"a":0}')
            self.assertEqual(read_mapping(path)[1],['a','b'])
            path.write_text('{"a":0,"b":2}')
            with self.assertRaises(ValueError):read_mapping(path)

    def test_pending_review_cannot_become_true(self):
        with self.assertRaises(ValueError):as_bool(pd.Series(['true','']))
        self.assertEqual(as_bool(pd.Series(['true','false'])).tolist(),[True,False])

if __name__=='__main__':unittest.main()
