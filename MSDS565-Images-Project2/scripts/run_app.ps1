# Run inside the conda environment used for Notebook 3.
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
python -m streamlit run app/P2_Images-5_App_Project2.py --server.address 127.0.0.1
