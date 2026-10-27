"""Auditable file handoffs only; notebook-specific analysis remains in each notebook."""
import hashlib
import json
import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app'))
from project_utils import resize_rgb, read_mapping


def load_config(require_confirmation=True):
    config = json.loads((ROOT / 'config/project.json').read_text(encoding='utf-8'))
    if require_confirmation and not config['classes_confirmed']:
        raise ValueError('Confirm actual classes and queries in config/project.json, then set classes_confirmed=true.')
    raw_path = os.environ.get('P2_DATA_ROOT', config['data_root'])
    if os.name != 'nt' and len(raw_path) > 1 and raw_path[1] == ':':
        raise OSError('This is a Windows data path. Run on Windows or set P2_DATA_ROOT to an accessible external directory.')
    data_root = Path(raw_path).expanduser().resolve()
    if data_root == ROOT or ROOT in data_root.parents:
        raise ValueError('Data, arrays, and images must be outside the Git repository.')
    data_root.mkdir(parents=True, exist_ok=True)
    return config, data_root


def digest(path):
    hasher = hashlib.sha256()
    with open(path, 'rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            hasher.update(block)
    return hasher.hexdigest()


def pixel_hash(image):
    """Catch identical decoded pixels even when file bytes/metadata differ."""
    rgb = ImageOps.exif_transpose(image).convert('RGB')
    return hashlib.sha256(str(rgb.size).encode() + rgb.tobytes()).hexdigest()


def dhash(image):
    """64-bit difference hash for human review, never an automatic subject judgment."""
    grey = np.asarray(ImageOps.exif_transpose(image).convert('L').resize((9, 8)))
    bits = (grey[:, 1:] > grey[:, :-1]).ravel()
    return sum(int(value) << index for index, value in enumerate(bits))


def as_bool(series):
    values = series.astype(str).str.lower().str.strip()
    if not values.isin(['true', 'false']).all():
        raise ValueError('Boolean columns must use true/false.')
    return values.eq('true')


def save_json(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(value, indent=2), encoding='utf-8')


def checked_manifest(config):
    path = ROOT / 'data/P2_manifest.csv'
    if not path.exists():
        raise FileNotFoundError('Run Notebook 1; existing folders require their real source manifest.')
    manifest = pd.read_csv(path, keep_default_na=False)
    required = {'filename', 'label', 'source_url', 'query', 'readable'}
    if not required.issubset(manifest):
        raise ValueError(f'Missing manifest columns: {required - set(manifest)}')
    if manifest.empty or manifest.duplicated(['label', 'filename']).any():
        raise ValueError('Manifest is empty or has duplicate image identifiers.')
    if set(manifest.label) != set(config['class_queries']):
        raise ValueError('Configured classes differ from manifest labels. Correct the class plan first.')
    for row in manifest.itertuples():
        # Neither a class nor a filename may escape the local image root.
        for value in [row.label, row.filename]:
            if '/' in value or '\\' in value or value in ['.', '..']:
                raise ValueError(f'Unsafe manifest path component: {value}')
    return manifest


def prepared_inputs(config, data_root):
    """Validate the split identity before exposing it to modeling or explanation."""
    prepared = data_root / 'prepared'
    meta = json.loads((prepared / 'preprocessing.json').read_text())
    if meta['manifest_sha256'] != digest(ROOT / 'data/P2_manifest.csv'):
        raise ValueError('Manifest changed since preprocessing. Re-run N2, then N3 and N4.')
    if meta['config_sha256'] != digest(ROOT / 'config/project.json'):
        raise ValueError('Config changed since preprocessing. Re-run N2 onward.')
    for filename, expected in meta['files_sha256'].items():
        if digest(prepared / filename) != expected:
            raise ValueError(f'Prepared file changed: {filename}')
    mapping, names = read_mapping(prepared / 'label_to_index.json')
    arrays = [np.load(prepared / f'{name}.npy', mmap_mode='r')
              for name in ['X_train', 'X_test', 'y_train', 'y_test']]
    return prepared, meta, mapping, names, arrays
