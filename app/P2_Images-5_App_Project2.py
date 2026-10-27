"""From the repository root: python -m streamlit run app/P2_Images-5_App_Project2.py."""
import hashlib
import json
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image, UnidentifiedImageError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'app'))
from deployment_utils import load_contract, prepare_upload, explain_one
from project_utils import join_model

st.set_page_config(page_title='Project 2: Image Classification', page_icon='🔨', layout='wide')
st.title('Project 2: Image Classification')
st.caption('One photograph. Three frozen image models. Their predictions and the regions behind them.')
try:
    metadata, geometry, mapping, class_names, fingerprint = load_contract(ROOT/'models')
except (OSError, ValueError, KeyError, TypeError) as error:
    st.error(f'The saved model package could not be verified: {error}')
    st.stop()

# Keep the user flow about the task; implementation explanations live below.
with st.sidebar:
    st.subheader('Hammer classes')
    for name in class_names:
        st.write('• ' + name.replace('-', ' ').title())
    st.caption('Upload a real photograph, a difficult example, or an unrelated object for comparison.')
    st.info('A softmax model always selects one of these three classes. A high score does not verify that the image contains a hammer.')
    st.caption('Uploads are processed in memory and are not saved to the dataset.')

with st.expander('Results from Notebooks 3 and 4'):
    comparison = pd.read_csv(ROOT/'models/P2_N3_comparison.csv')
    ablation = pd.read_csv(ROOT/'models/P2_N4_shortcut_ablation.csv')
    scores = comparison[['application','backbone_parameters','test_accuracy','macro_f1']].copy()
    scores['Parameters (millions)'] = scores.pop('backbone_parameters')/1e6
    scores['Test accuracy (%)'] = scores.pop('test_accuracy')*100
    scores['Macro-F1'] = scores.pop('macro_f1')
    st.dataframe(scores.rename(columns={'application':'Model'}).round(4), hide_index=True, use_container_width=True)
    st.caption('Recorded held-out split: 948 training and 238 test images. These are saved coursework results, not accuracy estimates for your new upload.')
    st.write('Covering the outer border reduced accuracy by ' + ', '.join(
        f"{row.application}: {row.accuracy_drop*100:.2f} percentage points" for row in ablation.itertuples()) + '.')
    st.caption('The mask covered 35.43% of pixels and may cover parts of the tool. This sensitivity result does not prove a shortcut. The uploaded Notebook 4 still has unfinished per-case review and deployment fields.')

upload = st.file_uploader('Upload an image', type=['jpg','jpeg','png','webp','bmp'], key='image_upload')
if upload is None:
    st.write('Choose a photograph to compare every model. No model selection is needed.')
    st.stop()
try:
    payload = upload.getvalue()
    original, raw = prepare_upload(payload, geometry)
except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError) as error:
    st.error(f'This image could not be prepared: {error}')
    st.stop()
left, right = st.columns([2,1])
left.image(original, caption='Uploaded image', width=360)
right.image(raw, caption='224 × 224 RGB input · original proportions preserved', width=224)
image_key = hashlib.sha256(payload + fingerprint.encode()).hexdigest()
if st.session_state.get('result_key') != image_key:
    st.session_state.pop('results', None)

@st.cache_resource(show_spinner=False)
def load_all_models(artifact_fingerprint):
    """Cache immutable trained models, never uploaded photographs."""
    del artifact_fingerprint
    return {name: join_model(name, ROOT/'models', tuple(geometry['target_size']))[0]
            for name in metadata['applications']}

if st.button('Compare all three models', type='primary'):
    try:
        with st.spinner('Loading the three trained models. The first run may download ImageNet weights…'):
            import image_explainers as xai
            models = load_all_models(fingerprint)
        results = {}
        progress = st.progress(0, text='Computing predictions and explanation maps…')
        for index, name in enumerate(metadata['applications']):
            with st.spinner(f'{name}: raw saliency, SmoothGrad (32 samples), and Grad-CAM…'):
                results[name] = explain_one(models[name], raw, xai)
            progress.progress((index+1)/len(models), text=f'{name} complete')
        st.session_state['results'] = results
        st.session_state['result_key'] = image_key
        progress.empty()
    except (ImportError, OSError, ValueError, RuntimeError, MemoryError) as error:
        st.error(f'Comparison could not finish: {error}')
        st.caption('Use the run guide to check dependencies, first-run weight downloads and available memory. All three models are required for the assignment.')

if st.session_state.get('result_key') == image_key and 'results' in st.session_state:
    import matplotlib.pyplot as plt
    results = st.session_state['results']
    winners = []
    for name in metadata['applications']:
        result = results[name]
        probabilities = result['probabilities']
        label = class_names[result['predicted']]
        winners.append(label)
        st.divider()
        st.subheader(name)
        columns = st.columns([1.45,1,1,1])
        with columns[0]:
            st.markdown(f'**{label.replace("-", " ").title()}**')
            st.metric('Highest class probability', f'{probabilities.max():.1%}')
            table = pd.DataFrame({'Class':class_names, 'Probability':probabilities}).sort_values('Probability',ascending=False)
            figure, axis = plt.subplots(figsize=(4.5,2.5))
            axis.barh(table['Class'].str.replace('-',' '), table['Probability'], color='#217b88')
            axis.invert_yaxis()
            axis.set_xlim(0,1)
            axis.set_xlabel('Softmax probability')
            for i, value in enumerate(table['Probability']):
                axis.text(min(value+.02,.98),i,f'{value:.1%}',ha='right' if value>.85 else 'left',va='center',fontsize=8)
            figure.tight_layout()
            st.pyplot(figure)
            plt.close(figure)
            st.caption(f"Normalized entropy: {result['entropy']:.3f} · explanation time: {result['seconds']:.1f}s")
        for column, caption, overlay in zip(columns[1:], ['Raw saliency','SmoothGrad · 32 samples','Grad-CAM'],result['overlays']):
            column.image(overlay, caption=caption, use_container_width=True)
    if len(set(winners)) == 1:
        st.write('All three models selected the same class. Agreement does not establish that the uploaded object belongs to the training classes.')
    else:
        st.write('The models disagree. Inspect the photograph, probability distributions and highlighted regions before trusting a label.')
    st.caption('Maps target each model’s predicted class. Grad-CAM starts at 7 × 7 spatial resolution. Colors are normalized separately; heat intensity cannot rank models. Entropy is not a validated unknown-object detector.')

with st.expander('How the app works and what to discuss in the demo'):
    st.markdown('''1. I apply the same RGB conversion, orientation, transparency handling and grey padding as Notebook 2.
2. I rebuild each frozen backbone and load its saved Notebook 3 classifier and class mapping.
3. I pass raw 0–255 pixels to the supplied explanation helper, which handles each model’s scaling once.
4. I show every model in its own row with sorted probabilities and all three overlays.
5. I test an ordinary photo, a hard case and an unrelated object. Unknown-object rejection would need separate data, validation and a calibrated decision rule.''')
