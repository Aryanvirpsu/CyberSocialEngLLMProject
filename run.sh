#!/bin/bash

echo "🚀 Starting CYBER 221 Project"

if [ -f "venv/bin/activate" ]; then
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️ Virtual environment not found. Running bootstrap..."
    python3 bootstrap.py
    source venv/bin/activate
fi

echo "📦 Running project..."
python3 main.py
