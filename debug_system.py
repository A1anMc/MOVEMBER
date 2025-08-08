#!/usr/bin/env python3
"""
Movember AI Rules System - Debugging Framework
Diagnoses and fixes common system issues
"""

import os
import sys
import sqlite3
import logging
import subprocess
import requests
import json
from datetime import datetime
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SystemDebugger:


    """Debugging framework for the Movember AI Rules System."""

    def __init__(self):


        self.issues = []
        self.fixes_applied = []
        self.system_status = {}

    def run_full_diagnostic(self):


        """Run comprehensive system diagnostics."""
        logger.info("🔍 Starting Movember AI Rules System Diagnostics...")

        # Check all components
        self.check_environment()
        self.check_dependencies()
        self.check_database()
        self.check_api()
        self.check_monitoring()
        self.check_scraper()
        self.check_logs()
        self.check_permissions()

        # Generate report
        self.generate_diagnostic_report()

    def check_environment(self):


        """Check Python environment and paths."""
        logger.info("🐍 Checking Python environment...")

        # Check Python version
        python_version = sys.version_info
        if python_version.major == 3 and python_version.minor >= 8:
            logger.info(f"✅ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
        else:
            self.issues.append("Python version should be 3.8+")
            logger.warning(f"⚠️ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")

        # Check virtual environment
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            logger.info("✅ Virtual environment is active")
        else:
            self.issues.append("Virtual environment not detected")
            logger.warning("⚠️ Virtual environment not detected")

        # Check current directory
        current_dir = os.getcwd()
        logger.info(f"📁 Current directory: {current_dir}")

        # Check required directories
        required_dirs = ['logs', 'api', 'rules', 'tests']
        for dir_name in required_dirs:
            if os.path.exists(dir_name):
                logger.info(f"✅ Directory exists: {dir_name}")
            else:
                self.issues.append(f"Missing directory: {dir_name}")
                logger.warning(f"⚠️ Missing directory: {dir_name}")
                # Create directory
                try:
                    os.makedirs(dir_name, exist_ok=True)
                    logger.info(f"✅ Created directory: {dir_name}")
                    self.fixes_applied.append(f"Created directory: {dir_name}")
                except Exception as e:
                    logger.error(f"❌ Failed to create directory {dir_name}: {e}")

    def check_dependencies(self):


        """Check required Python packages."""
        logger.info("📦 Checking dependencies...")

        required_packages = [
            'fastapi', 'uvicorn', 'sqlalchemy', 'aiohttp',
            'beautifulsoup4', 'httpx', 'pandas', 'pydantic',
            'requests', 'psutil'
        ]

        missing_packages = []
        for package in required_packages:
            try:
                __import__(package)
                logger.info(f"✅ Package available: {package}")
            except ImportError:
                missing_packages.append(package)
                logger.warning(f"⚠️ Missing package: {package}")

        if missing_packages:
            self.issues.append(f"Missing packages: {', '.join(missing_packages)}")
            logger.info("💡 Run: pip install " + " ".join(missing_packages))

    def check_database(self):


        """Check database integrity."""
        logger.info("💾 Checking database...")

        db_path = "movember_ai.db"
        if not os.path.exists(db_path):
            self.issues.append("Database file not found")
            logger.warning("⚠️ Database file not found")
            return

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Check tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]

            required_tables = [
                'grants', 'impact_reports', 'system_health',
                'scraped_data', 'monitoring_alerts', 'data_quality_reports', 'compliance_reports'
            ]

            for table in required_tables:
                if table in tables:
                    # Count records
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    logger.info(f"✅ Table {table}: {count} records")
                else:
                    self.issues.append(f"Missing table: {table}")
                    logger.warning(f"⚠️ Missing table: {table}")

            conn.close()
            logger.info("✅ Database connection successful")

        except Exception as e:
            self.issues.append(f"Database error: {str(e)}")
            logger.error(f"❌ Database error: {e}")

    def check_api(self):


        """Check API health."""
        logger.info("🌐 Checking API...")

        try:
            # Check if API is running
            response = requests.get("http://localhost: 8000/health/", timeout=5)
            if response.status_code == 200:
                logger.info("✅ API is running and healthy")
                self.system_status['api'] = 'healthy'
            else:
                self.issues.append(f"API returned status {response.status_code}")
                logger.warning(f"⚠️ API returned status {response.status_code}")
                self.system_status['api'] = 'error'
        except requests.exceptions.ConnectionError:
            self.issues.append("API not running")
            logger.warning("⚠️ API not running")
            self.system_status['api'] = 'stopped'
        except Exception as e:
            self.issues.append(f"API error: {str(e)}")
            logger.error(f"❌ API error: {e}")
            self.system_status['api'] = 'error'

    def check_monitoring(self):


        """Check monitoring bot status."""
        logger.info("🤖 Checking monitoring bot...")

        try:
            # Check if monitoring bot process is running
            result = subprocess.run(['pgrep', '-f', 'monitoring_bot.py'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                logger.info("✅ Monitoring bot is running")
                self.system_status['monitoring'] = 'running'
            else:
                logger.info("ℹ️ Monitoring bot is not running (optional)")
                self.system_status['monitoring'] = 'stopped'
        except Exception as e:
            logger.warning(f"⚠️ Could not check monitoring bot: {e}")
            self.system_status['monitoring'] = 'unknown'

    def check_scraper(self):


        """Check data scraper status."""
        logger.info("🕷️ Checking data scraper...")

        try:
            # Check if scraper process is running
            result = subprocess.run(['pgrep', '-f', 'data_scraper.py'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                logger.info("✅ Data scraper is running")
                self.system_status['scraper'] = 'running'
            else:
                logger.info("ℹ️ Data scraper is not running (optional)")
                self.system_status['scraper'] = 'stopped'
        except Exception as e:
            logger.warning(f"⚠️ Could not check data scraper: {e}")
            self.system_status['scraper'] = 'unknown'

    def check_logs(self):


        """Check log files."""
        logger.info("📁 Checking log files...")

        logs_dir = "logs"
        if not os.path.exists(logs_dir):
            self.issues.append("Logs directory not found")
            logger.warning("⚠️ Logs directory not found")
            return

        log_files = ['monitoring_bot.log', 'data_scraper.log']
        for log_file in log_files:
            log_path = os.path.join(logs_dir, log_file)
            if os.path.exists(log_path):
                size = os.path.getsize(log_path)
                logger.info(f"✅ Log file {log_file}: {size} bytes")
            else:
                logger.info(f"ℹ️ Log file {log_file}: not created yet")

    def check_permissions(self):


        """Check file permissions."""
        logger.info("🔐 Checking file permissions...")

        # Check executable scripts
        scripts = ['start_api.sh', 'start_monitoring.sh', 'start_scraper.sh',
                  'health_check.sh', 'system_status.sh']

        for script in scripts:
            if os.path.exists(script):
                if os.access(script, os.X_OK):
                    logger.info(f"✅ Script {script}: executable")
                else:
                    self.issues.append(f"Script {script} not executable")
                    logger.warning(f"⚠️ Script {script} not executable")
                    # Fix permissions
                    try:
                        os.chmod(script, 0o755)
                        logger.info(f"✅ Fixed permissions for {script}")
                        self.fixes_applied.append(f"Fixed permissions for {script}")
                    except Exception as e:
                        logger.error(f"❌ Failed to fix permissions for {script}: {e}")
            else:
                logger.warning(f"⚠️ Script not found: {script}")

    def generate_diagnostic_report(self):


        """Generate comprehensive diagnostic report."""
        logger.info("📊 Generating diagnostic report...")

        print("\n" + "="*60)
        print("🏥 MOVEMBER AI RULES SYSTEM - DIAGNOSTIC REPORT")
        print("="*60)

        # System status
        print(f"\n📈 System Status:")
        for component, status in self.system_status.items():
            status_icon = "✅" if status in ['healthy', 'running'] else "⚠️" if status == 'stopped' else "❌"
            print(f"  {status_icon} {component}: {status}")

        # Issues found
        if self.issues:
            print(f"\n🚨 Issues Found ({len(self.issues)}):")
            for i, issue in enumerate(self.issues, 1):
                print(f"  {i}. {issue}")
        else:
            print(f"\n✅ No issues found!")

        # Fixes applied
        if self.fixes_applied:
            print(f"\n🔧 Fixes Applied ({len(self.fixes_applied)}):")
            for i, fix in enumerate(self.fixes_applied, 1):
                print(f"  {i}. {fix}")

        # Recommendations
        print(f"\n💡 Recommendations:")
        if self.issues:
            print("  - Address the issues listed above")
            if "API not running" in str(self.issues):
                print("  - Start API: ./start_api.sh")
            if "Missing packages" in str(self.issues):
                print("  - Install missing packages: pip install <package_names>")
        else:
            print("  - System is healthy! No action required")
            print("  - Optional: Start monitoring bot for continuous monitoring")
            print("  - Optional: Start data scraper for data collection")

        print("\n" + "="*60)

        # Save report to file
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "system_status": self.system_status,
            "issues": self.issues,
            "fixes_applied": self.fixes_applied
        }

        with open("debug_report.json", "w") as f:
            json.dump(report_data, f, indent=2)

        logger.info("✅ Diagnostic report saved to debug_report.json")

def main():


    """Main debugging function."""
    debugger = SystemDebugger()
    debugger.run_full_diagnostic()

if __name__ == "__main__":
    main()
