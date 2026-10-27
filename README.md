# Project 2: Image Classification

I built a custom three-class hammer classifier and compared frozen MobileNetV2, ResNet50 and EfficientNetV2M backbones with trained single-Dense softmax probes. The Streamlit app shows every model's prediction, sorted class probabilities and three explanation overlays for an uploaded image.

**Start here:** [Windows app instructions](docs/RUN_STREAMLIT_WINDOWS.md). You can run the app directly from the supplied models; retraining and the external image dataset are not required for app inference.

## Classes and acquisition

| Class | Distinguishing feature | Exact queries |
|---|---|---|
| claw-hammer | Split claw opposite the striking face | claw hammer tool photograph; claw hammer workshop; claw hammer wooden handle |
| ball-peen-hammer | Rounded peen opposite the striking face | ball peen hammer tool photograph; ball pein hammer workshop; ball peen hammer wooden handle |
| sledgehammer | Broad, heavy, usually double-faced head | sledgehammer tool photograph; sledge hammer workshop; sledgehammer wooden handle |

These are related tool shapes, not a downloaded benchmark. Head geometry separates them, while angle, cropping and shared backgrounds create ambiguity. My pre-model prediction was greatest confusion between claw and ball-peen hammers because their rear head features can be hidden.

The supplied instructor scraper collected 400 images per class using multiple queries, Bing, 300 candidates/query, a minimum 224×224 resolution, aspect ratios 0.5–2.0 and 10-second download timeouts. The query-match guard stays on. Source URLs and queries are in `data/P2_manifest.csv`; images remain outside this repository.

The cleaning summary records 395 claw, 394 ball-peen and 397 sledgehammer images retained (1,186 total), split into 948 training and 238 test images. These are the supplied records, not a new certification of visual cleaning. Notebook 4 still shows some text-heavy and multi-object examples that warrant review.

## Pipeline and artifacts

| Order | File | Main output |
|---|---|---|
| 1 | notebooks/P2_Images-1_Scrape_Project2.ipynb | Acquisition manifest, exact queries, readability accounting and class plan |
| 2 | notebooks/P2_Images-2_Preprocessing_Project2.ipynb | Manual-cleaning accounting, image EDA, `kept` column; external raw uint8 RGB arrays and mapping |
| 3 | notebooks/P2_Images-3_TransferLearning_Project2.ipynb | Three trained probes, comparison metrics, reports, confusion tables and model metadata |
| 4 | notebooks/P2_Images-4_xAI_Project2.ipynb | Correct/error-case maps, same-image comparisons and border-occlusion results; final human review remains pending |
| 5 | app/P2_Images-5_App_Project2.py | Uploaded-image predictions and all three explanation maps, one model per row |

The saved preprocessing contract is 224×224 RGB, EXIF orientation, transparency composited onto grey, aspect-preserving Lanczos resize/padding with RGB (127,127,127), and raw uint8 0–255 pixels. The app uses the same `project_utils.resize_rgb` function and passes the raw image directly to the unchanged `image_explainers.py`. Model-specific scaling happens once, inside that helper.

## Recorded results

| Model | Backbone parameters (without classification top) | Test accuracy | Macro-F1 | Border-occlusion drop |
|---|---:|---:|---:|---:|
| MobileNetV2 | 2,257,984 | 90.34% | 0.9035 | 8.82 percentage points |
| ResNet50 | 23,587,712 | 93.70% | 0.9370 | 11.34 percentage points |
| EfficientNetV2M | 53,150,388 | 94.54% | 0.9453 | 7.56 percentage points |

These values come from `models/P2_N3_comparison.csv` and `models/P2_N4_shortcut_ablation.csv`. Covering the border masks 35.43% of pixels and can cover tools too; the drops are sensitivity measurements, not proof of background shortcuts. All three CAM grids are 7×7. A high softmax probability is not evidence that an unrelated upload belongs to a hammer class.

## Run the app

In Anaconda PowerShell Prompt, activate the environment used for Notebook 3, open this repository root, then run:

```powershell
conda activate msds565
python -m pip install streamlit==1.42.2
python -m streamlit run app/P2_Images-5_App_Project2.py
```

Open `http://localhost:8501`, upload a photograph, and click **Compare all three models**. The first comparison downloads the three pretrained ImageNet backbones if they are not in the Keras cache. Later comparisons reuse them. Keep this terminal open; stop the app with Ctrl+C.

The app runs locally and does not require GitHub Pages, public hosting, or a dataset upload. For a new environment, follow the run guide. `requirements-app.txt` is the app-only installation path; `environment.yml` is currently a reconstructed setup, **not** the required export from the actual Windows notebook environment.

## Repository organization

```text
MSDS565-Images-Project2/
  README.md
  environment.yml
  requirements-app.txt
  data/          # source manifest and aggregate CSV/JSON evidence; no images
  models/        # supplied small trained probes, mappings and result tables
  notebooks/     # four canonical notebooks and supplied helpers
  app/           # Streamlit entrypoint, shared preprocessing and supplied helper
  docs/          # run guide, live-demo guide, GitHub steps and submission status
  scripts/       # environment export, launch and validation
  tests/         # app and preprocessing checks
  .streamlit/    # local server and theme settings; no credentials
```

The filename token is `Project2` wherever the prompt uses `<TeamName>`. It contains no student's name and does not use Team 1. The displayed project title remains **Project 2: Image Classification**. Three probe files are under 100 KB each; Git LFS is unnecessary. Pretrained backbones download into the Keras cache outside the repository.

The four notebooks retain their executed outputs, as the prompt requires. Images embedded in those required outputs remain in the notebooks; there are no standalone scraped/cleaned image files or `.npy` arrays in this package. Do not add `Images.zip`, `Images/raw`, `Images/prepared`, caches or checkpoints.
