# Run in Anaconda PowerShell Prompt from the extracted repository root.
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
conda env create -f environment.yml
if ($LASTEXITCODE -ne 0) { throw 'Conda environment creation failed.' }
conda run -n project2-image-classification python -m ipykernel install --user --name project2-image-classification --display-name 'Python (project2-image-classification)'
if ($LASTEXITCODE -ne 0) { throw 'Kernel registration failed.' }
Write-Host 'Edit config/project.json to confirm your actual classes before opening Notebook 1.'
Write-Host 'Activate with: conda activate project2-image-classification'
Write-Host 'Launch with: jupyter lab'
