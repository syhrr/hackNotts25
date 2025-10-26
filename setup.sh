#!/bin/bash

echo "========================================"
echo "Medieval D&D Chatbot - Quick Setup"
echo "========================================"
echo ""

echo "[1/4] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment"
    echo "Make sure Python 3 is installed"
    exit 1
fi

echo "[2/4] Activating virtual environment..."
source venv/bin/activate

echo "[3/4] Installing dependencies..."
cd backend
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo "[4/4] Creating .env file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo ".env file created! Edit backend/.env if you want to add an OpenAI API key."
else
    echo ".env file already exists, skipping..."
fi

cd ..

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To start the game, run:"
echo "  ./start.sh"
echo ""
echo "Or manually:"
echo "  1. cd backend"
echo "  2. python main.py"
echo "  3. Open frontend/index.html in browser"
echo ""