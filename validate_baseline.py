#!/usr/bin/env python3
"""
Movember AI Rules System - Baseline Validation
Compares current system state against baseline configuration
"""

import os
import sys
import json
import sqlite3
import requests
import subprocess
from datetime import datetime
from typing import Dict, List, Any

class BaselineValidator:
    """Validates system against baseline configuration."""
    
    def __init__(self, baseline_file: str = "baseline_config.json"):
        self.baseline_file = baseline_file
        self.baseline = self.load_baseline()
        self.validation_results = {
            "passed": [],
            "failed": [],
            "warnings": [],
            "timestamp": datetime.now().isoformat()
        }
    
    def load_baseline(self) -> Dict[str, Any]:
        """Load baseline configuration."""
        try:
            with open(self.baseline_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Baseline file not found: {self.baseline_file}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid baseline file: {e}")
            sys.exit(1)
    
    def validate_system(self):
        """Run comprehensive baseline validation."""
        print("🔍 Validating Movember AI Rules System against baseline...")
        
        self.validate_environment()
        self.validate_directories()
        self.validate_files()
        self.validate_dependencies()
        self.validate_database()
        self.validate_api()
        self.validate_compliance()
        self.validate_monitoring()
        self.validate_performance()
        
        self.generate_validation_report()
    
    def validate_environment(self):
        """Validate Python environment."""
        print("\n🐍 Validating Python environment...")
        
        # Check Python version
        python_version = sys.version_info
        required_version = (3, 8)
        if python_version >= required_version:
            self.validation_results["passed"].append("Python version >= 3.8")
            print(f"✅ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
        else:
            self.validation_results["failed"].append(f"Python version {python_version.major}.{python_version.minor} < 3.8")
            print(f"❌ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        # Check virtual environment
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            self.validation_results["passed"].append("Virtual environment active")
            print("✅ Virtual environment is active")
        else:
            self.validation_results["failed"].append("Virtual environment not active")
            print("❌ Virtual environment not active")
    
    def validate_directories(self):
        """Validate required directories."""
        print("\n📁 Validating directories...")
        
        required_dirs = self.baseline["system_baseline"]["directories"]["required"]
        optional_dirs = self.baseline["system_baseline"]["directories"]["optional"]
        
        for dir_name in required_dirs:
            if os.path.exists(dir_name):
                self.validation_results["passed"].append(f"Directory exists: {dir_name}")
                print(f"✅ {dir_name}")
            else:
                self.validation_results["failed"].append(f"Missing required directory: {dir_name}")
                print(f"❌ {dir_name}")
        
        for dir_name in optional_dirs:
            if os.path.exists(dir_name):
                self.validation_results["passed"].append(f"Optional directory exists: {dir_name}")
                print(f"✅ {dir_name} (optional)")
            else:
                self.validation_results["warnings"].append(f"Optional directory missing: {dir_name}")
                print(f"⚠️ {dir_name} (optional)")
    
    def validate_files(self):
        """Validate required files."""
        print("\n📄 Validating files...")
        
        core_files = self.baseline["system_baseline"]["files"]["core"]
        script_files = self.baseline["system_baseline"]["files"]["scripts"]
        test_files = self.baseline["system_baseline"]["files"]["tests"]
        
        for file_name in core_files:
            if os.path.exists(file_name):
                self.validation_results["passed"].append(f"Core file exists: {file_name}")
                print(f"✅ {file_name}")
            else:
                self.validation_results["failed"].append(f"Missing core file: {file_name}")
                print(f"❌ {file_name}")
        
        for file_name in script_files:
            if os.path.exists(file_name):
                if os.access(file_name, os.X_OK):
                    self.validation_results["passed"].append(f"Script exists and executable: {file_name}")
                    print(f"✅ {file_name}")
                else:
                    self.validation_results["warnings"].append(f"Script not executable: {file_name}")
                    print(f"⚠️ {file_name} (not executable)")
            else:
                self.validation_results["failed"].append(f"Missing script: {file_name}")
                print(f"❌ {file_name}")
        
        for file_name in test_files:
            if os.path.exists(file_name):
                self.validation_results["passed"].append(f"Test file exists: {file_name}")
                print(f"✅ {file_name}")
            else:
                self.validation_results["warnings"].append(f"Missing test file: {file_name}")
                print(f"⚠️ {file_name}")
    
    def validate_dependencies(self):
        """Validate Python dependencies."""
        print("\n📦 Validating dependencies...")
        
        required_packages = self.baseline["system_baseline"]["dependencies"]["required"]
        optional_packages = self.baseline["system_baseline"]["dependencies"]["optional"]
        
        for package in required_packages:
            try:
                __import__(package)
                self.validation_results["passed"].append(f"Required package available: {package}")
                print(f"✅ {package}")
            except ImportError:
                self.validation_results["failed"].append(f"Missing required package: {package}")
                print(f"❌ {package}")
        
        for package in optional_packages:
            try:
                __import__(package)
                self.validation_results["passed"].append(f"Optional package available: {package}")
                print(f"✅ {package} (optional)")
            except ImportError:
                self.validation_results["warnings"].append(f"Missing optional package: {package}")
                print(f"⚠️ {package} (optional)")
    
    def validate_database(self):
        """Validate database."""
        print("\n💾 Validating database...")
        
        db_path = "movember_ai.db"
        if not os.path.exists(db_path):
            self.validation_results["failed"].append("Database file not found")
            print("❌ Database file not found")
            return
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = [row[0] for row in cursor.fetchall()]
            required_tables = self.baseline["system_baseline"]["database"]["tables"]
            
            for table in required_tables:
                if table in existing_tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    self.validation_results["passed"].append(f"Table exists: {table} ({count} records)")
                    print(f"✅ {table} ({count} records)")
                else:
                    self.validation_results["failed"].append(f"Missing table: {table}")
                    print(f"❌ {table}")
            
            conn.close()
            self.validation_results["passed"].append("Database connection successful")
            print("✅ Database connection successful")
            
        except Exception as e:
            self.validation_results["failed"].append(f"Database error: {str(e)}")
            print(f"❌ Database error: {e}")
    
    def validate_api(self):
        """Validate API endpoints."""
        print("\n🌐 Validating API...")
        
        expected_endpoints = self.baseline["system_baseline"]["api"]["endpoints"]
        api_port = self.baseline["system_baseline"]["api"]["port"]
        
        try:
            # Check if API is running
            response = requests.get(f"http://localhost:{api_port}/health/", timeout=5)
            if response.status_code == 200:
                self.validation_results["passed"].append("API is running and healthy")
                print("✅ API is running and healthy")
                
                # Check endpoints
                for endpoint in expected_endpoints:
                    try:
                        response = requests.get(f"http://localhost:{api_port}{endpoint}", timeout=5)
                        if response.status_code == 200:
                            self.validation_results["passed"].append(f"Endpoint accessible: {endpoint}")
                            print(f"✅ {endpoint}")
                        else:
                            self.validation_results["warnings"].append(f"Endpoint returned {response.status_code}: {endpoint}")
                            print(f"⚠️ {endpoint} ({response.status_code})")
                    except Exception as e:
                        self.validation_results["warnings"].append(f"Endpoint error: {endpoint} - {str(e)}")
                        print(f"⚠️ {endpoint} (error)")
            else:
                self.validation_results["failed"].append(f"API returned status {response.status_code}")
                print(f"❌ API returned status {response.status_code}")
        except requests.exceptions.ConnectionError:
            self.validation_results["failed"].append("API not running")
            print("❌ API not running")
        except Exception as e:
            self.validation_results["failed"].append(f"API error: {str(e)}")
            print(f"❌ API error: {e}")
    
    def validate_compliance(self):
        """Validate compliance standards."""
        print("\n🔍 Validating compliance standards...")
        
        # Test UK spelling conversion
        try:
            from data_scraper import MovemberDataScraper
            scraper = MovemberDataScraper()
            test_text = "This uses American spelling like color and center"
            uk_text = scraper.convert_to_uk_spelling(test_text)
            
            if "colour" in uk_text and "centre" in uk_text:
                self.validation_results["passed"].append("UK spelling conversion working")
                print("✅ UK spelling conversion working")
            else:
                self.validation_results["failed"].append("UK spelling conversion not working")
                print("❌ UK spelling conversion not working")
        except Exception as e:
            self.validation_results["failed"].append(f"UK spelling test failed: {str(e)}")
            print(f"❌ UK spelling test failed: {e}")
        
        # Test AUD currency formatting
        try:
            from data_scraper import MovemberDataScraper
            scraper = MovemberDataScraper()
            test_amount = 50000.00
            aud_formatted = scraper.format_aud_currency(test_amount)
            
            if aud_formatted.startswith("A$"):
                self.validation_results["passed"].append("AUD currency formatting working")
                print("✅ AUD currency formatting working")
            else:
                self.validation_results["failed"].append("AUD currency formatting not working")
                print("❌ AUD currency formatting not working")
        except Exception as e:
            self.validation_results["failed"].append(f"AUD currency test failed: {str(e)}")
            print(f"❌ AUD currency test failed: {e}")
    
    def validate_monitoring(self):
        """Validate monitoring components."""
        print("\n🤖 Validating monitoring...")
        
        # Check monitoring bot
        try:
            result = subprocess.run(['pgrep', '-f', 'monitoring_bot.py'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.validation_results["passed"].append("Monitoring bot is running")
                print("✅ Monitoring bot is running")
            else:
                self.validation_results["warnings"].append("Monitoring bot not running")
                print("⚠️ Monitoring bot not running")
        except Exception as e:
            self.validation_results["warnings"].append(f"Could not check monitoring bot: {str(e)}")
            print(f"⚠️ Could not check monitoring bot: {e}")
        
        # Check data scraper
        try:
            result = subprocess.run(['pgrep', '-f', 'data_scraper.py'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.validation_results["passed"].append("Data scraper is running")
                print("✅ Data scraper is running")
            else:
                self.validation_results["warnings"].append("Data scraper not running")
                print("⚠️ Data scraper not running")
        except Exception as e:
            self.validation_results["warnings"].append(f"Could not check data scraper: {str(e)}")
            print(f"⚠️ Could not check data scraper: {e}")
    
    def validate_performance(self):
        """Validate performance metrics."""
        print("\n📈 Validating performance...")
        
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            if cpu_percent < 80:
                self.validation_results["passed"].append(f"CPU usage acceptable: {cpu_percent:.1f}%")
                print(f"✅ CPU usage: {cpu_percent:.1f}%")
            else:
                self.validation_results["warnings"].append(f"High CPU usage: {cpu_percent:.1f}%")
                print(f"⚠️ CPU usage: {cpu_percent:.1f}%")
            
            if memory.percent < 85:
                self.validation_results["passed"].append(f"Memory usage acceptable: {memory.percent:.1f}%")
                print(f"✅ Memory usage: {memory.percent:.1f}%")
            else:
                self.validation_results["warnings"].append(f"High memory usage: {memory.percent:.1f}%")
                print(f"⚠️ Memory usage: {memory.percent:.1f}%")
                
        except Exception as e:
            self.validation_results["warnings"].append(f"Could not check performance: {str(e)}")
            print(f"⚠️ Could not check performance: {e}")
    
    def generate_validation_report(self):
        """Generate validation report."""
        print("\n" + "="*60)
        print("📊 BASELINE VALIDATION REPORT")
        print("="*60)
        
        total_checks = len(self.validation_results["passed"]) + len(self.validation_results["failed"]) + len(self.validation_results["warnings"])
        
        print(f"\n📈 Summary:")
        print(f"  ✅ Passed: {len(self.validation_results['passed'])}")
        print(f"  ❌ Failed: {len(self.validation_results['failed'])}")
        print(f"  ⚠️ Warnings: {len(self.validation_results['warnings'])}")
        print(f"  📊 Total: {total_checks}")
        
        if self.validation_results["failed"]:
            print(f"\n❌ Critical Issues:")
            for issue in self.validation_results["failed"]:
                print(f"  - {issue}")
        
        if self.validation_results["warnings"]:
            print(f"\n⚠️ Warnings:")
            for warning in self.validation_results["warnings"]:
                print(f"  - {warning}")
        
        # Overall status
        if not self.validation_results["failed"]:
            print(f"\n🎉 Status: EXCELLENT - All critical checks passed!")
        elif len(self.validation_results["failed"]) <= 2:
            print(f"\n🟡 Status: GOOD - Minor issues detected")
        else:
            print(f"\n🔴 Status: NEEDS ATTENTION - Multiple critical issues")
        
        print("\n" + "="*60)
        
        # Save report
        with open("baseline_validation_report.json", "w") as f:
            json.dump(self.validation_results, f, indent=2)
        
        print("✅ Validation report saved to baseline_validation_report.json")

def main():
    """Main validation function."""
    validator = BaselineValidator()
    validator.validate_system()

if __name__ == "__main__":
    main() 