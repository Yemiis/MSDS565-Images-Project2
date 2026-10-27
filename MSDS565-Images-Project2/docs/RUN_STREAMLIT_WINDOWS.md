# Run the Streamlit app on Windows

## Use your working notebook environment

1. Download and extract `MSDS565-Images-Project2.zip`. Place the extracted `MSDS565-Images-Project2` folder beside your existing `Images` folder. Keep your original project as a backup. The app reads its included `models` folder; it does not need the dataset path.
2. Open **Anaconda PowerShell Prompt**. Do not paste these commands into a Python code cell.
3. Activate the environment you used for Notebook 3:

```powershell
conda activate msds565
```

If your working environment has a different name, use that name. `conda env list` lists available environments. The recorded Notebook 3 versions are Python 3.12.12, TensorFlow 2.20.0 and Keras 3.15.0.

4. Open the extracted repository root:

```powershell
cd "C:\Users\lawra\Fall 2026-2027 Semester Document\MSDS 565-01\Project 2 Image Classification\MSDS565-Images-Project2"
Test-Path .\app\P2_Images-5_App_Project2.py
Test-Path .\models\training_metadata.json
```

Both checks should print `True`. If not, use the directory containing this README, `app`, `models` and `notebooks`.

5. Install Streamlit in the active environment, then verify it:

```powershell
python -m pip install streamlit==1.42.2
python -c "import sys, tensorflow as tf, keras, streamlit; print(sys.executable); print(tf.__version__, keras.__version__, streamlit.__version__)"
```

Expected framework versions: `2.20.0 3.15.0 1.42.2`. Do not retrain or overwrite model metadata just to launch the app. If your existing notebook environment already works, install only the missing Streamlit dependency.

6. Start the app:

```powershell
python -m streamlit run app/P2_Images-5_App_Project2.py
```

7. Open **http://localhost:8501**. Keep the PowerShell window open. Upload a JPG, JPEG, PNG, WebP or BMP, then click **Compare all three models**.
8. On the first comparison, Keras may download about 300 MB of pretrained backbone weights into your user cache. This requires internet access. Once cached, no dataset or web search is needed. All three models and 32-sample SmoothGrad can take time on a CPU; follow the progress indicator.
9. Each model gets one row: prediction, all three probabilities sorted highest first, raw saliency, SmoothGrad and Grad-CAM. Prepare an ordinary hammer photograph, a hard example and an unrelated photograph for the live demo.
10. Stop with **Ctrl+C** in PowerShell. Restart using the same command. Replacing any trained artifacts requires restarting the process to avoid stale models.

## If creating a separate environment

This does not replace the instructor's required export of your original notebook environment.

```powershell
conda create -n project2-image-classification python=3.12 pip -y
conda activate project2-image-classification
python -m pip install -r requirements-app.txt
python -m streamlit run app/P2_Images-5_App_Project2.py
```

Alternatively, `conda env create -f environment.yml` installs the reconstructed full notebook setup. It is labeled as reconstructed because a true Windows conda export was not supplied.

## Export your actual environment before GitHub submission

After activating the environment actually used for the notebooks and adding Streamlit:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\export_environment.ps1
```

Or use the exact assignment command:

```powershell
conda env export --no-builds > environment.yml
```

The script removes only the machine-specific `prefix:` and writes UTF-8 without a BOM. It accepts `msds565`; it no longer incorrectly requires a newly named environment.

## Troubleshooting

| Symptom | Action |
|---|---|
| `No module named streamlit` | Activate the notebook environment; install with `python -m pip`, then use `python -m streamlit`. |
| Script not found | Return to the extracted repository root and repeat the two `Test-Path` checks. |
| Port 8501 is busy | Stop the older app or add `--server.port 8502`; open the corresponding localhost URL. |
| Model hash mismatch | Restore the matching probe and training metadata from one Notebook 3 run. Do not edit hashes. |
| Download cannot finish | Allow Keras to download pretrained weights, then retry. Offline operation needs those weights cached first. |
| First comparison is slow | All three models run and SmoothGrad uses 32 samples per model. CPU inference is supported; no GPU is required. |
| Image rejected | Use a decodable image under 20 MB and 25 million pixels. The unchanged helper also rejects almost entirely black inputs. |
| High score for an unrelated object | This is expected behavior from a closed-set classifier; the app discloses it and does not pretend to reject unknowns. |
| Notebook asks for external arrays | Only notebook reruns require `Images/prepared`. The app uses included deployment metadata and probes. |
