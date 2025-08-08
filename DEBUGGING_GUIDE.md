# 🔧 Movember AI Rules System - Debugging & Baseline Guide

## 🎯 **Overview**

This guide explains how to debug the Movember AI Rules System and create a solid baseline for development and deployment.

## 🔍 **Debugging Framework**

### **1. Quick Debug Script** (`quick_debug.sh`)
**Purpose**: Rapid diagnosis and fix of common issues
**Usage**: `./quick_debug.sh`

**What it checks:**
- ✅ Directory structure
- ✅ Python environment
- ✅ Dependencies (FastAPI, SQLAlchemy, Requests, etc.)
- ✅ Database file
- ✅ API health
- ✅ Script permissions
- ✅ Logs directory
- ✅ System tests

**Example output:**
```bash
🔧 Movember AI Rules System - Quick Debug
==========================================

📁 Directory check:
  ✅ In correct Movember AI Rules System directory

🐍 Python environment:
  ✅ Virtual environment active

📦 Dependencies:
  ✅ All packages available

💾 Database:
  ✅ Database file exists

🌐 API:
  ✅ API is running and healthy

🧪 Quick system test:
  ✅ Monitoring test passed
  ✅ Scraper test passed
```

### **2. Comprehensive Debug System** (`debug_system.py`)
**Purpose**: Detailed system diagnostics with fixes
**Usage**: `python debug_system.py`

**What it checks:**
- 🐍 Python environment and version
- 📁 Directory structure validation
- 📦 Package dependency verification
- 💾 Database integrity and tables
- 🌐 API health and endpoints
- 🤖 Monitoring bot status
- 🕷️ Data scraper status
- 📁 Log file analysis
- 🔐 File permissions

**Example output:**
```bash
🏥 MOVEMBER AI RULES SYSTEM - DIAGNOSTIC REPORT
============================================================

📈 System Status:
  ✅ api: healthy
  ⚠️ monitoring: stopped
  ⚠️ scraper: stopped

🚨 Issues Found (3):
  1. Missing packages: beautifulsoup4
  2. Missing table: scraped_data
  3. Missing table: monitoring_alerts

💡 Recommendations:
  - Address the issues listed above
  - Install missing packages: pip install <package_names>
```

### **3. Baseline Validation** (`validate_baseline.py`)
**Purpose**: Compare system against baseline configuration
**Usage**: `python validate_baseline.py`

**What it validates:**
- 🐍 Python environment compliance
- 📁 Directory structure against baseline
- 📄 File existence and permissions
- 📦 Dependency versions
- 💾 Database schema and tables
- 🌐 API endpoints and responses
- 🔍 Compliance standards (UK spelling, AUD currency)
- 🤖 Monitoring components
- 📈 Performance metrics

**Example output:**
```bash
📊 BASELINE VALIDATION REPORT
============================================================

📈 Summary:
  ✅ Passed: 48
  ❌ Failed: 3
  ⚠️ Warnings: 4
  📊 Total: 55

🎉 Status: EXCELLENT - All critical checks passed!
```

## 📋 **Baseline Configuration**

### **Baseline File** (`baseline_config.json`)
**Purpose**: Defines expected system state

**Key sections:**
```json
{
  "system_baseline": {
    "version": "1.1.0",
    "environment": {
      "python_version": "3.8+",
      "virtual_environment": "required"
    },
    "directories": {
      "required": ["api", "rules", "tests", "logs", "docs", "scripts"],
      "optional": ["backups", "config", "database"]
    },
    "files": {
      "core": ["simple_api.py", "monitoring_bot.py", "data_scraper.py"],
      "scripts": ["start_api.sh", "start_monitoring.sh", "start_scraper.sh"]
    },
    "dependencies": {
      "required": ["fastapi", "uvicorn", "sqlalchemy", "aiohttp"],
      "optional": ["prometheus-client", "structlog"]
    },
    "compliance": {
      "uk_spelling": {"enabled": true},
      "aud_currency": {"enabled": true}
    }
  }
}
```

## 🛠️ **Common Issues & Solutions**

### **1. API Not Running**
**Symptoms**: Connection refused, API not responding
**Solutions**:
```bash
# Start the API
./start_api.sh

# Check if port 8000 is available
lsof -i :8000

# Verify virtual environment
source venv/bin/activate
```

### **2. Database Issues**
**Symptoms**: Database not found, Table missing
**Solutions**:
```bash
# Check database file
ls -la movember_ai.db

# Initialize database
python -c "import sqlite3; conn = sqlite3.connect('movember_ai.db'); conn.close()"

# Check tables
sqlite3 movember_ai.db ".tables"
```

### **3. Dependency Issues**
**Symptoms**: ModuleNotFoundError, ImportError
**Solutions**:
```bash
# Install missing packages
pip install fastapi uvicorn sqlalchemy aiohttp beautifulsoup4 httpx pandas pydantic requests psutil

# Check installed packages
pip list

# Verify virtual environment
which python
```

### **4. Permission Issues**
**Symptoms**: Permission denied, Not executable
**Solutions**:
```bash
# Fix script permissions
chmod +x *.sh

# Check file ownership
ls -la *.sh

# Verify directory permissions
ls -la
```

### **5. Monitoring Bot Issues**
**Symptoms**: Bot not running, Log errors
**Solutions**:
```bash
# Start monitoring bot
./start_monitoring.sh

# Check logs
tail -f logs/monitoring_bot.log

# Test monitoring
python test_monitoring.py
```

### **6. Data Scraper Issues**
**Symptoms**: Scraper not running, Import errors
**Solutions**:
```bash
# Start data scraper
./start_scraper.sh

# Test scraper
python test_scraper.py

# Check dependencies
pip install beautifulsoup4 aiohttp httpx
```

## 🔧 **Debugging Workflow**

### **Step 1: Quick Assessment**
```bash
./quick_debug.sh
```
- Identifies obvious issues
- Applies automatic fixes
- Provides status summary

### **Step 2: Detailed Diagnostics**
```bash
python debug_system.py
```
- Comprehensive system analysis
- Detailed issue reporting
- Fix recommendations

### **Step 3: Baseline Validation**
```bash
python validate_baseline.py
```
- Compares against baseline
- Validates compliance standards
- Performance assessment

### **Step 4: Issue Resolution**
Based on diagnostic results:
1. **Install missing dependencies**: `pip install <package>`
2. **Fix permissions**: `chmod +x *.sh`
3. **Start services**: `./start_api.sh`, `./start_monitoring.sh`
4. **Check logs**: `tail -f logs/*.log`

## 📊 **System Health Indicators**

### **🟢 EXCELLENT**
- All critical checks passed
- No issues detected
- System fully operational

### **🟡 GOOD**
- Minor issues detected
- Core functionality working
- Optional components may be stopped

### **🔴 NEEDS ATTENTION**
- Critical issues detected
- Core functionality affected
- Immediate action required

## 📈 **Performance Benchmarks**

### **API Performance**
- Response time: < 1 second
- Health check: 200 OK
- All endpoints accessible

### **Database Performance**
- Query time: < 100ms
- All tables present
- Connection successful

### **System Performance**
- CPU usage: < 80%
- Memory usage: < 85%
- Disk usage: < 90%

## 🔍 **Advanced Debugging**

### **Log Analysis**
```bash
# View all logs
tail -f logs/*.log

# Search for errors
grep -i error logs/*.log

# Monitor API logs
tail -f logs/api.log
```

### **Database Debugging**
```bash
# Check database schema
sqlite3 movember_ai.db ".schema"

# Check table contents
sqlite3 movember_ai.db "SELECT * FROM system_health LIMIT 5;"

# Check table counts
sqlite3 movember_ai.db "SELECT name, COUNT(*) FROM sqlite_master WHERE type='table';"
```

### **Network Debugging**
```bash
# Check API endpoints
curl -v http://localhost:8000/health/

# Test all endpoints
for endpoint in / /health/ /grants/ /metrics/; do
  curl -s -o /dev/null -w "%{http_code}" http://localhost:8000$endpoint
done
```

## 🎯 **Creating a Baseline**

### **1. Establish Current State**
```bash
# Run comprehensive diagnostics
python debug_system.py

# Validate against baseline
python validate_baseline.py

# Save current configuration
cp baseline_config.json baseline_config_backup.json
```

### **2. Document Working Configuration**
- Update `baseline_config.json` with current working state
- Document any customizations or environment-specific settings
- Note any deviations from standard configuration

### **3. Create Baseline Snapshot**
```bash
# Create baseline snapshot
tar -czf baseline_snapshot_$(date +%Y%m%d).tar.gz \
  *.py *.sh *.json *.db logs/ api/ rules/ tests/
```

### **4. Validate Baseline**
```bash
# Test baseline configuration
python validate_baseline.py

# Ensure all tests pass
python test_monitoring.py
python test_scraper.py
```

## 🚀 **Production Readiness Checklist**

### **✅ Core Requirements**
- [ ] API running and healthy
- [ ] Database accessible and complete
- [ ] Virtual environment active
- [ ] All dependencies installed
- [ ] Scripts executable
- [ ] Logs directory exists

### **✅ Compliance Standards**
- [ ] UK spelling conversion working
- [ ] AUD currency formatting working
- [ ] Data quality validation active
- [ ] Framework compliance (ToC, CEMP, SDG)

### **✅ Monitoring & Maintenance**
- [ ] Monitoring bot operational
- [ ] Data scraper functional
- [ ] Health checks passing
- [ ] Performance within limits
- [ ] Error handling active

### **✅ Security & Reliability**
- [ ] Input validation active
- [ ] Error handling comprehensive
- [ ] Rate limiting configured
- [ ] Backup procedures in place

## 📚 **Additional Resources**

### **Documentation**
- `README.md` - System overview
- `FEATURES_SUMMARY.md` - Feature documentation
- `baseline_config.json` - Configuration reference

### **Scripts**
- `quick_debug.sh` - Rapid diagnosis
- `debug_system.py` - Comprehensive diagnostics
- `validate_baseline.py` - Baseline validation
- `system_status.sh` - System status overview

### **Tests**
- `test_monitoring.py` - Monitoring functionality test
- `test_scraper.py` - Scraper functionality test
- `test_rules_system.py` - Rules system test

**The Movember AI Rules System now has a comprehensive debugging and baseline framework for reliable development and deployment!** 🎉 