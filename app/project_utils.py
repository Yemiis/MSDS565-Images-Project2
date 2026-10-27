"""Shared image geometry and model constructors. No training occurs on import."""
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageOps


def resize_rgb(image, size=(224, 224), padding=(127, 127, 127)):
    """Orient, flatten transparency on grey, convert to RGB, and pad without distortion."""
    image = ImageOps.exif_transpose(image)
    rgba = image.convert('RGBA')
    background = Image.new('RGBA', rgba.size, tuple(padding) + (255,))
    rgb = Image.alpha_composite(background, rgba).convert('RGB')
    # Pillow size is (width, height); config size is (height, width).
    output = ImageOps.pad(rgb, (size[1], size[0]), method=Image.Resampling.LANCZOS,
                          color=tuple(padding), centering=(0.5, 0.5))
    return np.asarray(output, dtype=np.uint8)


def application_spec(name):
    """Resolve canonical names so N3, N4, and the app cannot choose different models."""
    import keras
    specs = {
        'mobilenetv2': (keras.applications.MobileNetV2,
                        keras.applications.mobilenet_v2.preprocess_input),
        'resnet50': (keras.applications.ResNet50,
                     keras.applications.resnet50.preprocess_input),
        'efficientnetv2m': (keras.applications.EfficientNetV2M,
                            keras.applications.efficientnet_v2.preprocess_input),
    }
    if name not in specs:
        raise ValueError(f'Unknown application: {name}')
    return specs[name]


def build_application(name, size):
    """Use untouched ImageNet weights, global average pooling, and frozen layers."""
    constructor, preprocess = application_spec(name)
    model = constructor(weights='imagenet', include_top=False, pooling='avg',
                        input_shape=(*size, 3))
    model.trainable = False
    return model, preprocess


def join_model(name, model_dir, size):
    """Join the exact frozen application to its saved linear probe; xai scales inputs."""
    import keras
    base, _ = build_application(name, size)
    probe = keras.models.load_model(Path(model_dir) / f'P2_N3_{name}.keras')
    if probe.input_shape[-1] != base.output_shape[-1]:
        raise ValueError('Embedding dimension does not match the saved probe.')
    return keras.Sequential([keras.Input((*size, 3)), base, probe]), base


def read_mapping(path):
    """Reject non-contiguous indices before a wrong mapping can rename predictions."""
    mapping = json.loads(Path(path).read_text(encoding='utf-8'))
    if sorted(mapping.values()) != list(range(len(mapping))):
        raise ValueError('Label mapping must contain contiguous indices from zero.')
    return mapping, [label for label, index in sorted(mapping.items(), key=lambda item: item[1])]
