#!/bin/bash

# Movember AI Rules System - Comprehensive Status Check
# Shows status of all system components

echo "🏥 Movember AI Rules System - System Status"
echo "=============================================="
echo ""

# Check API status
echo "🌐 API Status:"
if curl -f -s http://localhost:8000/health/ > /dev/null; then
    echo "  ✅ API is running and healthy"
    API_STATUS="RUNNING"
else
    echo "  ❌ API is not responding"
    API_STATUS="STOPPED"
fi

# Check database
echo ""
echo "💾 Database Status:"
if [ -f "movember_ai.db" ]; then
    echo "  ✅ Database file exists"
    DB_SIZE=$(du -h movember_ai.db | cut -f1)
    echo "  📊 Database size: $DB_SIZE"
    DB_STATUS="EXISTS"
else
    echo "  ❌ Database file not found"
    DB_STATUS="MISSING"
fi

# Check virtual environment
echo ""
echo "🐍 Python Environment:"
if [ -d "venv" ]; then
    echo "  ✅ Virtual environment exists"
    VENV_STATUS="EXISTS"
else
    echo "  ❌ Virtual environment not found"
    VENV_STATUS="MISSING"
fi

# Check monitoring bot
echo ""
echo "🤖 Monitoring Bot:"
if pgrep -f "monitoring_bot.py" > /dev/null; then
    echo "  ✅ Monitoring bot is running"
    BOT_STATUS="RUNNING"
else
    echo "  ❌ Monitoring bot is not running"
    BOT_STATUS="STOPPED"
fi

# Check data scraper
echo ""
echo "🕷️ Data Scraper:"
if pgrep -f "data_scraper.py" > /dev/null; then
    echo "  ✅ Data scraper is running"
    SCRAPER_STATUS="RUNNING"
else
    echo "  ❌ Data scraper is not running"
    SCRAPER_STATUS="STOPPED"
fi

# Check logs
echo ""
echo "📁 Logs:"
if [ -d "logs" ]; then
    echo "  ✅ Logs directory exists"
    LOG_COUNT=$(find logs -name "*.log" | wc -l)
    echo "  📊 Log files: $LOG_COUNT"
    LOG_STATUS="EXISTS"
else
    echo "  ❌ Logs directory not found"
    LOG_STATUS="MISSING"
fi

# Check recent data
echo ""
echo "📊 Recent Data:"
if [ "$DB_STATUS" = "EXISTS" ]; then
    # Count grants
    GRANT_COUNT=$(sqlite3 movember_ai.db "SELECT COUNT(*) FROM grants;" 2>/dev/null || echo "0")
    echo "  📋 Grants: $GRANT_COUNT"
    
    # Count reports
    REPORT_COUNT=$(sqlite3 movember_ai.db "SELECT COUNT(*) FROM impact_reports;" 2>/dev/null || echo "0")
    echo "  📄 Reports: $REPORT_COUNT"
    
    # Count scraped data
    SCRAPED_COUNT=$(sqlite3 movember_ai.db "SELECT COUNT(*) FROM scraped_data;" 2>/dev/null || echo "0")
    echo "  🕷️ Scraped records: $SCRAPED_COUNT"
    
    # Count alerts
    ALERT_COUNT=$(sqlite3 movember_ai.db "SELECT COUNT(*) FROM monitoring_alerts;" 2>/dev/null || echo "0")
    echo "  🚨 Alerts: $ALERT_COUNT"
else
    echo "  ❌ Cannot access database"
fi

# System health summary
echo ""
echo "=============================================="
echo "🏥 System Health Summary:"
echo ""

if [ "$API_STATUS" = "RUNNING" ] && [ "$DB_STATUS" = "EXISTS" ] && [ "$VENV_STATUS" = "EXISTS" ]; then
    echo "  ✅ Core system is healthy"
    CORE_HEALTH="HEALTHY"
else
    echo "  ❌ Core system has issues"
    CORE_HEALTH="UNHEALTHY"
fi

if [ "$BOT_STATUS" = "RUNNING" ]; then
    echo "  ✅ Monitoring is active"
    MONITORING_HEALTH="ACTIVE"
else
    echo "  ⚠️ Monitoring is inactive"
    MONITORING_HEALTH="INACTIVE"
fi

if [ "$SCRAPER_STATUS" = "RUNNING" ]; then
    echo "  ✅ Data collection is active"
    SCRAPING_HEALTH="ACTIVE"
else
    echo "  ⚠️ Data collection is inactive"
    SCRAPING_HEALTH="INACTIVE"
fi

# Overall status
echo ""
echo "🎯 Overall System Status:"
if [ "$CORE_HEALTH" = "HEALTHY" ] && [ "$MONITORING_HEALTH" = "ACTIVE" ]; then
    echo "  🟢 EXCELLENT - All systems operational"
elif [ "$CORE_HEALTH" = "HEALTHY" ]; then
    echo "  🟡 GOOD - Core system healthy, monitoring optional"
else
    echo "  🔴 NEEDS ATTENTION - Core system issues detected"
fi

echo ""
echo "🛠️ Management Commands:"
echo "  - Start API: ./start_api.sh"
echo "  - Start Monitoring: ./start_monitoring.sh"
echo "  - Start Scraper: ./start_scraper.sh"
echo "  - Health Check: ./health_check.sh"
echo "  - View Logs: tail -f logs/*.log"
echo ""
echo "🌐 System URLs:"
echo "  - API: http://localhost:8000/"
echo "  - Health: http://localhost:8000/health/"
echo "  - Metrics: http://localhost:8000/metrics/"
echo "==============================================" 