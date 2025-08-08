#!/bin/bash

# Health check for Movember AI Rules System

API_URL="http://localhost:8000/health/"
LOG_DIR="$HOME/movember-ai-rules/logs"

echo "🏥 Movember AI Rules System Health Check"
echo "=========================================="

# Check if API is running
if curl -f -s "$API_URL" > /dev/null; then
    echo "✅ API is healthy"
else
    echo "❌ API health check failed"
    echo "   Try starting the API: ./start_api.sh"
fi

# Check if database exists
if [ -f "movember_ai.db" ]; then
    echo "✅ Database exists"
else
    echo "❌ Database not found"
fi

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "✅ Virtual environment exists"
else
    echo "❌ Virtual environment not found"
fi

# Check log files
if [ -d "$LOG_DIR" ]; then
    echo "✅ Log directory exists"
else
    echo "❌ Log directory not found"
fi

echo "=========================================="
echo "🌐 API: http://localhost:8000/"
echo "📋 Health: http://localhost:8000/health/"
echo "📊 Metrics: http://localhost:8000/metrics/"
echo "==========================================" 