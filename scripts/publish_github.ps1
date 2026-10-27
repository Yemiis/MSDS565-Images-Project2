# Run only when ready to publish the source package yourself.
# GitHub CLI is optional; see docs/GITHUB_UPLOAD.md for browser steps.
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
python scripts/validate_project.py
if ($LASTEXITCODE -ne 0) { throw 'Fix package validation failures before publishing.' }
if (-not (Test-Path .git)) { git init -b main }
git add .
git diff --cached --stat
Write-Host 'Review the staged files above. Dataset images and arrays must remain outside this repository.'
# Leave commit, remote selection and push explicit; no account authorization is assumed.
Write-Host 'Next: git commit -m "Add Project 2 image classification app and notebooks"'
Write-Host 'Then use the exact remote URL from your newly created private GitHub repository.'
