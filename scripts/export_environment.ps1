# Run after activating the environment actually used for the notebooks.
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
if (-not $env:CONDA_DEFAULT_ENV -or $env:CONDA_DEFAULT_ENV -eq 'base') {
    throw 'Activate the notebook environment first (for example, conda activate msds565).'
}
$export = conda env export --no-builds
if ($LASTEXITCODE -ne 0) { throw 'Conda export failed; existing environment.yml preserved.' }
# Write real newlines as UTF-8 without a machine-specific prefix or BOM.
$lines = $export | Where-Object { $_ -notmatch '^prefix:' }
[System.IO.File]::WriteAllText((Join-Path (Get-Location) 'environment.yml'), ($lines -join "`n") + "`n", [System.Text.UTF8Encoding]::new($false))
Write-Host "Exported actual active environment: $env:CONDA_DEFAULT_ENV"
