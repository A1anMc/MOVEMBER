#!/bin/bash

# Movember Impact Dashboard Startup Script
echo "🎯 Starting Movember Impact Dashboard..."

# Check if API is running
if ! curl -s http://localhost:8000/health/ > /dev/null 2>&1; then
    echo "🚀 Starting API server..."
    python simple_api.py &
    API_PID=$!
    echo "✅ API server started (PID: $API_PID)"
    sleep 3
else
    echo "✅ API server already running"
fi

# Start frontend server
echo "🌐 Starting frontend server..."
cd frontend
python server.py &
FRONTEND_PID=$!
cd ..

echo ""
echo "🎉 Movember Impact Dashboard is ready!"
echo "📊 API: http://localhost:8000"
echo "🌐 Dashboard: http://localhost:3000"
echo ""
echo "📋 Available endpoints:"
echo "   • /impact/global/ - Global impact data"
echo "   • /impact/executive-summary/ - Executive summary"
echo "   • /impact/dashboard/ - Dashboard data"
echo "   • /impact/category/{category}/ - Category-specific data"
echo ""
echo "⏹️  Press Ctrl+C to stop all servers"

# Wait for user to stop
trap "echo '🛑 Stopping servers...'; kill $API_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait 