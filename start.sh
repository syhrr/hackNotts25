#!/bin/bash

echo ""
echo "========================================"
echo "   MEDIEVAL D&D CHATBOT"
echo "   One-Click Startup"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[!] Virtual environment not found!"
    echo "[!] Please run ./setup.sh first"
    echo ""
    exit 1
fi

echo "[*] Activating virtual environment..."
source venv/bin/activate

echo "[*] Starting backend server..."
cd backend
python main.py &
BACKEND_PID=$!
cd ..

sleep 3

echo "[*] Starting frontend server..."
cd frontend
python -m http.server 8080 &
FRONTEND_PID=$!
cd ..

sleep 2

echo "[*] Opening game in browser..."
if command -v xdg-open > /dev/null; then
    xdg-open http://localhost:8080
elif command -v open > /dev/null; then
    open http://localhost:8080
else
    echo "Please open http://localhost:8080 in your browser"
fi

echo ""
echo "========================================"
echo "   Game is now running!"
echo "========================================"
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:8080"
echo ""
echo "Press CTRL+C to stop all servers..."
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "[*] Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "[*] Servers stopped. Goodbye!"
    exit 0
}

# Set trap to cleanup on CTRL+C
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait