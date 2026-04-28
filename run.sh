#!/bin/bash

# Exit on error
set -e

echo "🎙️ Journalist Interview Transcriber — Launcher"
echo "============================================="

# 1. Check for ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ Error: ffmpeg is not installed."
    echo "   macOS: brew install ffmpeg"
    echo "   Linux: sudo apt install ffmpeg"
    exit 1
fi

# 2. Setup Virtual Environment
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

echo "Activating virtual environment..."
source .venv/bin/activate

# 3. Install/Update dependencies
echo "Installing dependencies (this may take a minute)..."
pip install -r requirements.txt --quiet

# 4. Launch App
echo "🚀 Launching Web UI..."
streamlit run app.py
