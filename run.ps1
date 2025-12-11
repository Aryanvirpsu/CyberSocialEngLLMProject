Write-Host "🚀 Starting CYBER 221 Project"

# Activate venv if it exists
if (Test-Path "venv\Scripts\activate.ps1") {
    Write-Host "🔧 Activating virtual environment..."
    . .\venv\Scripts\activate.ps1
} else {
    Write-Host "⚠️ Virtual environment not found. Running bootstrap..."
    python .\bootstrap.py
    . .\venv\Scripts\activate.ps1
}

Write-Host "📦 Running project..."
python main.py
