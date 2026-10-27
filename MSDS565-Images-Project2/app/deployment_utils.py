"""App-only artifact validation and inference; never loads the training dataset."""
import hashlib
import json
from io import BytesIO
from pathlib import Path
import threading
import numpy as np
from PIL import Image
from project_utils import resize_rgb, read_mapping

MODEL_NAMES = ('mobilenetv2', 'resnet50', 'efficientnetv2m')
INFERENCE_LOCK = threading.Lock()


def digest_file(path):
    """Stream a SHA-256 without copying a whole model into memory."""
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def load_contract(model_dir):
    """Reject mismatched probes, geometry or class order before predicting."""
    model_dir = Path(model_dir)
    metadata = json.loads((model_dir/'training_metadata.json').read_text(encoding='utf-8-sig'))
    geometry = json.loads((model_dir/'preprocessing.json').read_text(encoding='utf-8-sig'))
    mapping, names = read_mapping(model_dir/'label_to_index.json')
    if tuple(metadata['applications']) != MODEL_NAMES:
        raise ValueError('Expected all three Notebook 3 applications in their saved order.')
    if (geometry['resize_strategy'] != 'pad' or geometry['color_mode'] != 'RGB'
            or geometry['dtype'] != 'uint8' or geometry['range'] != [0, 255]
            or geometry['target_size'] != [224, 224]):
        raise ValueError('The saved preprocessing contract differs from Notebook 2.')
    if len(names) != 3:
        raise ValueError('The trained probes require the saved three-class mapping.')
    for name in MODEL_NAMES:
        path = model_dir/f'P2_N3_{name}.keras'
        if digest_file(path) != metadata['probe_sha256'][name]:
            raise ValueError(f'{name}: saved model differs from Notebook 3 metadata. Restore matching artifacts; do not overwrite the hash.')
    if digest_file(model_dir/'preprocessing.json') != metadata['preprocessing_sha256']:
        raise ValueError('Preprocessing metadata differs from Notebook 3.')
    if digest_file(model_dir/'label_to_index.json') != geometry['files_sha256']['label_to_index.json']:
        raise ValueError('Saved label order differs from Notebook 2.')
    fingerprint = hashlib.sha256(json.dumps({
        'probes': metadata['probe_sha256'], 'preprocessing':metadata['preprocessing_sha256']
    }, sort_keys=True).encode()).hexdigest()
    return metadata, geometry, mapping, names, fingerprint


def prepare_upload(payload, geometry):
    """Decode in memory and call exactly the same geometry function as N2."""
    if len(payload) > 20*1024*1024:
        raise ValueError('Please upload an image smaller than 20 MB.')
    with Image.open(BytesIO(payload)) as image:
        # Bound decoded size before loading the pixel data.
        if image.width*image.height > 25_000_000:
            raise ValueError('Please reduce the image to fewer than 25 million pixels.')
        image.load()
        raw = resize_rgb(image, tuple(geometry['target_size']), tuple(geometry['padding_rgb']))
        original = image.convert('RGB').copy()
    if raw.max() <= 1:
        raise ValueError('The supplied explanation helper rejects an almost entirely black input. Use a photograph with visible content.')
    return original, raw


def explain_one(model, raw, xai):
    """Pass raw pixels once; supplied xai handles model-specific scaling."""
    import time
    start = time.perf_counter()
    # Serialize shared models and seeded NumPy noise across browser sessions.
    with INFERENCE_LOCK:
        state = np.random.get_state()
        try:
            np.random.seed(42)
            probabilities = np.asarray(xai.predict_proba(model, raw), dtype=float)
            if probabilities.ndim != 1 or not np.isfinite(probabilities).all():
                raise ValueError('Model returned invalid class probabilities.')
            if not np.isclose(probabilities.sum(), 1, atol=1e-5):
                raise ValueError('Model probabilities do not sum to one.')
            predicted = int(probabilities.argmax())
            maps = [xai.saliency(model, raw, class_index=predicted),
                    xai.saliency(model, raw, smooth=32, class_index=predicted),
                    xai.grad_cam(model, raw, class_index=predicted)]
            for heat in maps:
                if np.asarray(heat).shape != raw.shape[:2] or not np.isfinite(heat).all():
                    raise ValueError('Explanation map has an invalid shape or non-finite values.')
            overlays = [xai.overlay(raw, heat) for heat in maps]
        finally:
            np.random.set_state(state)
    entropy = float(-(probabilities*np.log(np.clip(probabilities,1e-12,1))).sum()/np.log(len(probabilities)))
    return {'probabilities':probabilities,'predicted':predicted,'overlays':overlays,
            'entropy':entropy,'seconds':time.perf_counter()-start}
