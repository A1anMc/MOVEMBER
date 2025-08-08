#!/bin/bash

# Movember AI Rules System - Quick Debug Script
# Rapidly diagnose and fix common issues

echo "🔧 Movember AI Rules System - Quick Debug"
echo "=========================================="

# Function to check and fix common issues
check_and_fix() {
    local issue="$1"
    local check_cmd="$2"
    local fix_cmd="$3"
    
    echo "🔍 Checking: $issue"
    if eval "$check_cmd" >/dev/null 2>&1; then
        echo "  ✅ OK"
    else
        echo "  ❌ Issue detected"
        if [ -n "$fix_cmd" ]; then
            echo "  🔧 Applying fix..."
            eval "$fix_cmd"
            if eval "$check_cmd" >/dev/null 2>&1; then
                echo "  ✅ Fixed"
            else
                echo "  ❌ Fix failed"
            fi
        fi
    fi
}

# Check if we're in the right directory
echo ""
echo "📁 Directory check:"
if [ -f "simple_api.py" ] && [ -f "movember_ai.db" ]; then
    echo "  ✅ In correct Movember AI Rules System directory"
else
    echo "  ❌ Not in Movember AI Rules System directory"
    echo "  💡 Navigate to the project directory first"
    exit 1
fi

# Check virtual environment
echo ""
echo "🐍 Python environment:"
check_and_fix "Virtual environment" \
    "source venv/bin/activate && python -c 'import sys; print(sys.prefix)'" \
    "echo 'Please activate virtual environment: source venv/bin/activate'"

# Check dependencies
echo ""
echo "📦 Dependencies:"
check_and_fix "FastAPI" \
    "python -c 'import fastapi'" \
    "pip install fastapi uvicorn"

check_and_fix "SQLAlchemy" \
    "python -c 'import sqlalchemy'" \
    "pip install sqlalchemy"

check_and_fix "Requests" \
    "python -c 'import requests'" \
    "pip install requests"

check_and_fix "BeautifulSoup4" \
    "python -c 'import bs4'" \
    "pip install beautifulsoup4"

check_and_fix "aiohttp" \
    "python -c 'import aiohttp'" \
    "pip install aiohttp"

check_and_fix "psutil" \
    "python -c 'import psutil'" \
    "pip install psutil"

# Check database
echo ""
echo "💾 Database:"
check_and_fix "Database file exists" \
    "test -f movember_ai.db" \
    "python -c \"import sqlite3; conn = sqlite3.connect('movember_ai.db'); conn.close(); print('Database created')\""

# Check API
echo ""
echo "🌐 API:"
check_and_fix "API is running" \
    "curl -f http://localhost:8000/health/ >/dev/null 2>&1" \
    "echo 'Start API with: ./start_api.sh'"

# Check scripts
echo ""
echo "🛠️ Scripts:"
check_and_fix "Scripts are executable" \
    "test -x start_api.sh" \
    "chmod +x *.sh"

# Check logs directory
echo ""
echo "📁 Logs:"
check_and_fix "Logs directory exists" \
    "test -d logs" \
    "mkdir -p logs"

# Quick system test
echo ""
echo "🧪 Quick system test:"
if python test_monitoring.py >/dev/null 2>&1; then
    echo "  ✅ Monitoring test passed"
else
    echo "  ❌ Monitoring test failed"
fi

if python test_scraper.py >/dev/null 2>&1; then
    echo "  ✅ Scraper test passed"
else
    echo "  ❌ Scraper test failed"
fi

# Final status
echo ""
echo "📊 Quick Debug Summary:"
echo "  - Run: ./system_status.sh for detailed status"
echo "  - Run: python debug_system.py for comprehensive diagnostics"
echo "  - Run: python validate_baseline.py for baseline validation"
echo ""
echo "🛠️ Common Commands:"
echo "  - Start API: ./start_api.sh"
echo "  - Health check: ./health_check.sh"
echo "  - System status: ./system_status.sh"
echo "  - Start monitoring: ./start_monitoring.sh"
echo "  - Start scraper: ./start_scraper.sh"
echo ""
echo "==========================================" 