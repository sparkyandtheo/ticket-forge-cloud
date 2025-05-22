$venv = ".\venv\Scripts\Activate.ps1"

if (Test-Path $venv) {
    Write-Host "Activating venv..."
    & $venv
} else {
    Write-Host "❌ Virtual environment activation script not found at $venv"
}
