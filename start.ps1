$ErrorActionPreference = "Stop"
$py = "C:\Users\harih\AppData\Local\Programs\Python\Python312\python.exe"

Write-Host "Creating virtual environment..."
& $py -m venv venv

Write-Host "Activating virtual environment..."
$env:VIRTUAL_ENV = "$PWD\venv"
$env:PATH = "$PWD\venv\Scripts;$env:PATH"

Write-Host "Installing backend dependencies..."
cd backend
python -m pip install -r requirements.txt

Write-Host "Starting FastAPI backend..."
Start-Process -FilePath "uvicorn.exe" -ArgumentList "main:app --reload" -WindowStyle Hidden

Write-Host "Installing frontend dependencies..."
cd ..\frontend
python -m pip install -r requirements.txt

Write-Host "Starting Streamlit frontend..."
Start-Process -FilePath "streamlit.exe" -ArgumentList "run app.py" -WindowStyle Hidden

Write-Host "Done!"
