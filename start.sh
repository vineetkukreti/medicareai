#!/bin/bash

# MediCareAI Quick Start Script
# This script helps you set up and run the MediCareAI application

echo "🏥 MediCareAI Setup Script"
echo "=========================="
echo ""

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp backend/.env.example backend/.env
    echo "✅ Created backend/.env file"
    echo ""
    echo "⚠️  IMPORTANT: You need to add your Google Gemini API key!"
    echo "   1. Get your API key from: https://makersuite.google.com/app/apikey"
    echo "   2. Edit backend/.env and add: GEMINI_API_KEY=your_key_here"
    echo ""
    read -p "Press Enter after you've added your API key..."
fi

echo "📦 Installing backend dependencies..."
cd backend
source venv/bin/activate
pip install -q -r requirements.txt
cd ..
echo "✅ Backend dependencies installed"
echo ""

echo "📦 Installing frontend dependencies..."
cd frontend
if [ ! -d "node_modules" ]; then
    npm install
else
    echo "✅ Frontend dependencies already installed"
fi
cd ..
echo ""

echo "🚀 Starting MediCareAI..."
echo ""
echo "Starting backend server..."
cd backend
source venv/bin/activate
uvicorn app.main:app --reload &
BACKEND_PID=$!
cd ..

echo "Waiting for backend to start..."
sleep 3

echo "Starting frontend server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ MediCareAI is now running!"
echo ""
echo "📍 Frontend: http://localhost:5173"
echo "📍 Backend:  http://localhost:8000"
echo "📍 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
