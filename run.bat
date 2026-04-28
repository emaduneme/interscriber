@echo off
echo 🎙️ Journalist Interview Transcriber — Launcher
echo =============================================

:: 1. Check for ffmpeg
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: ffmpeg is not installed or not in PATH.
    echo Please install ffmpeg to continue.
    pause
    exit /b
)

:: 2. Setup Virtual Environment
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

echo Activating virtual environment...
call .venv\Scripts\activate

:: 3. Install/Update dependencies
echo Installing dependencies (this may take a minute)...
pip install -r requirements.txt --quiet

:: 4. Launch App
echo 🚀 Launching Web UI...
streamlit run app.py
pause
