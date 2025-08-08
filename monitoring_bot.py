#!/usr/bin/env python3
"""
Movember AI Rules System - Monitoring Bot
Continuously monitors system health, data quality, and compliance standards
"""

import asyncio
import logging
import sqlite3
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import time
import psutil
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/monitoring_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MovemberMonitoringBot:


    """Monitoring bot for the Movember AI Rules System."""

    def __init__(self, api_url: str = "http://localhost: 8000", check_interval: int = 60):


        self.api_url = api_url
        self.check_interval = check_interval
        self.db_path = "movember_ai.db"
        self.alerts = []
        self.metrics_history = []

    async def start_monitoring(self):
        """Start the monitoring bot."""
        logger.info("🤖 Starting Movember Monitoring Bot...")

        while True:
            try:
                await self.run_health_checks()
                await self.check_data_quality()
                await self.validate_compliance()
                await self.collect_system_metrics()
                await self.generate_alerts()

                logger.info(f"✅ Monitoring cycle completed at {datetime.now()}")
                await asyncio.sleep(self.check_interval)

            except Exception as e:
                logger.error(f"❌ Monitoring cycle failed: {e}")
                await asyncio.sleep(10)  # Shorter wait on error

    async def run_health_checks(self):
        """Check system health endpoints."""
        logger.info("🏥 Running health checks...")

        checks = {
            "api_health": f"{self.api_url}/health/",
            "api_root": f"{self.api_url}/",
            "metrics": f"{self.api_url}/metrics/",
            "grants": f"{self.api_url}/grants/",
        }

        health_status = {}

        for check_name, url in checks.items():
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    health_status[check_name] = "healthy"
                    logger.info(f"✅ {check_name}: Healthy")
                else:
                    health_status[check_name] = f"error_{response.status_code}"
                    logger.warning(f"⚠️ {check_name}: Error {response.status_code}")
            except Exception as e:
                health_status[check_name] = f"failed_{str(e)}"
                logger.error(f"❌ {check_name}: Failed - {e}")

        # Store health status
        await self.store_health_metrics(health_status)

    async def check_data_quality(self):
        """Check data quality in the database."""
        logger.info("📊 Checking data quality...")

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Check grants data quality
            cursor.execute("""
                SELECT
                    COUNT(*) as total_grants,
                    COUNT(CASE WHEN currency = 'AUD' THEN 1 END) as aud_compliant,
                    COUNT(CASE WHEN budget > 0 THEN 1 END) as valid_budgets,
                    COUNT(CASE WHEN title IS NOT NULL AND title != '' THEN 1 END) as valid_titles
                FROM grants
            """)
            grant_stats = cursor.fetchone()

            # Check reports data quality
            cursor.execute("""
                SELECT
                    COUNT(*) as total_reports,
                    COUNT(CASE WHEN frameworks IS NOT NULL AND frameworks != '' THEN 1 END) as valid_frameworks,
                    COUNT(CASE WHEN title IS NOT NULL AND title != '' THEN 1 END) as valid_titles
                FROM impact_reports
            """)
            report_stats = cursor.fetchone()

            conn.close()

            # Calculate quality scores
            grant_quality = (grant_stats[1] / max(grant_stats[0], 1)) * 100  # AUD compliance
            report_quality = (report_stats[1] / max(report_stats[0], 1)) * 100  # Framework compliance

            quality_metrics = {
                "grants": {
                    "total": grant_stats[0],
                    "aud_compliant": grant_stats[1],
                    "valid_budgets": grant_stats[2],
                    "valid_titles": grant_stats[3],
                    "quality_score": grant_quality
                },
                "reports": {
                    "total": report_stats[0],
                    "valid_frameworks": report_stats[1],
                    "valid_titles": report_stats[2],
                    "quality_score": report_quality
                }
            }

            logger.info(f"📊 Data quality - Grants: {grant_quality:.1f}%, Reports: {report_quality:.1f}%")
            await self.store_quality_metrics(quality_metrics)

        except Exception as e:
            logger.error(f"❌ Data quality check failed: {e}")

    async def validate_compliance(self):
        """Validate UK spelling and AUD currency compliance."""
        logger.info("🔍 Validating compliance standards...")

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Check UK spelling in grants
            cursor.execute("SELECT data_json FROM grants")
            grant_data = cursor.fetchall()

            uk_spelling_issues = 0
            aud_currency_issues = 0

            american_spellings = ['color', 'favor', 'center', 'theater', 'realize', 'organize', 'analyze']

            for row in grant_data:
                if row[0]:
                    data = json.loads(row[0])
                    description = data.get('description', '').lower()

                    # Check for American spellings
                    for spelling in american_spellings:
                        if spelling in description:
                            uk_spelling_issues += 1
                            break

                    # Check currency
                    if data.get('currency', '').upper() != 'AUD':
                        aud_currency_issues += 1

            # Check reports
            cursor.execute("SELECT data_json FROM impact_reports")
            report_data = cursor.fetchall()

            for row in report_data:
                if row[0]:
                    data = json.loads(row[0])
                    description = data.get('description', '').lower()

                    for spelling in american_spellings:
                        if spelling in description:
                            uk_spelling_issues += 1
                            break

            conn.close()

            total_records = len(grant_data) + len(report_data)
            uk_compliance = ((total_records - uk_spelling_issues) / max(total_records, 1)) * 100
            aud_compliance = ((len(grant_data) - aud_currency_issues) / max(len(grant_data), 1)) * 100

            compliance_metrics = {
                "uk_spelling_issues": uk_spelling_issues,
                "aud_currency_issues": aud_currency_issues,
                "uk_spelling_compliance": uk_compliance,
                "aud_currency_compliance": aud_compliance,
                "total_records_checked": total_records
            }

            logger.info(f"🔍 Compliance - UK Spelling: {uk_compliance:.1f}%, AUD Currency: {aud_compliance:.1f}%")
            await self.store_compliance_metrics(compliance_metrics)

        except Exception as e:
            logger.error(f"❌ Compliance validation failed: {e}")

    async def collect_system_metrics(self):
        """Collect system performance metrics."""
        logger.info("📈 Collecting system metrics...")

        try:
            # System metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            # Process metrics
            process = psutil.Process()
            process_memory = process.memory_info().rss / 1024 / 1024  # MB

            system_metrics = {
                "timestamp": datetime.now().isoformat(),
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_gb": memory.available / 1024 / 1024 / 1024,
                "disk_percent": disk.percent,
                "disk_free_gb": disk.free / 1024 / 1024 / 1024,
                "process_memory_mb": process_memory,
                "uptime_seconds": time.time() - process.create_time()
            }

            logger.info(f"📈 System - CPU: {cpu_percent:.1f}%, Memory: {memory.percent:.1f}%, Disk: {disk.percent:.1f}%")
            await self.store_system_metrics(system_metrics)

        except Exception as e:
            logger.error(f"❌ System metrics collection failed: {e}")

    async def generate_alerts(self):
        """Generate alerts based on thresholds."""
        logger.info("🚨 Checking for alerts...")

        alerts = []

        # Check system health
        if len(self.metrics_history) > 0:
            latest_metrics = self.metrics_history[-1]

            # CPU alert
            if latest_metrics.get('cpu_percent', 0) > 80:
                alerts.append({
                    "type": "high_cpu",
                    "severity": "warning",
                    "message": f"High CPU usage: {latest_metrics['cpu_percent']:.1f}%",
                    "timestamp": datetime.now().isoformat()
                })

            # Memory alert
            if latest_metrics.get('memory_percent', 0) > 85:
                alerts.append({
                    "type": "high_memory",
                    "severity": "warning",
                    "message": f"High memory usage: {latest_metrics['memory_percent']:.1f}%",
                    "timestamp": datetime.now().isoformat()
                })

            # Disk alert
            if latest_metrics.get('disk_percent', 0) > 90:
                alerts.append({
                    "type": "low_disk",
                    "severity": "critical",
                    "message": f"Low disk space: {latest_metrics['disk_percent']:.1f}% used",
                    "timestamp": datetime.now().isoformat()
                })

        # Store alerts
        if alerts:
            await self.store_alerts(alerts)
            for alert in alerts:
                logger.warning(f"🚨 {alert['severity'].upper()}: {alert['message']}")
        else:
            logger.info("✅ No alerts generated")

    async def store_health_metrics(self, health_status: Dict[str, str]):
        """Store health metrics in database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO system_health (
                    timestamp, system_status, uk_spelling_consistency, aud_currency_compliance
                ) VALUES (?, ?, ?, ?)
            """, (
                datetime.now(),
                json.dumps(health_status),
                1.0 if all(status == "healthy" for status in health_status.values()) else 0.0,
                1.0  # Will be updated by compliance check
            ))

            conn.commit()
            conn.close()

        except Exception as e:
            logger.error(f"❌ Failed to store health metrics: {e}")

    async def store_quality_metrics(self, quality_metrics: Dict[str, Any]):
        """Store data quality metrics."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Create data quality table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS data_quality_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    report_id TEXT UNIQUE NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total_records INTEGER,
                    valid_records INTEGER,
                    invalid_records INTEGER,
                    uk_spelling_issues INTEGER,
                    aud_currency_issues INTEGER,
                    quality_score REAL,
                    report_json TEXT
                )
            """)

            report_id = f"DQ_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            total_records = quality_metrics['grants']['total'] + quality_metrics['reports']['total']
            valid_records = quality_metrics['grants']['valid_titles'] + quality_metrics['reports']['valid_titles']

            cursor.execute("""
                INSERT INTO data_quality_reports (
                    report_id, total_records, valid_records, invalid_records,
                    quality_score, report_json
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                report_id,
                total_records,
                valid_records,
                total_records - valid_records,
                (quality_metrics['grants']['quality_score'] + quality_metrics['reports']['quality_score']) / 2,
                json.dumps(quality_metrics)
            ))

            conn.commit()
            conn.close()

        except Exception as e:
            logger.error(f"❌ Failed to store quality metrics: {e}")

    async def store_compliance_metrics(self, compliance_metrics: Dict[str, Any]):
        """Store compliance metrics."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Create compliance table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS compliance_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total_rules INTEGER,
                    uk_spelling_compliance REAL,
                    aud_currency_compliance REAL,
                    overall_compliance REAL,
                    report_json TEXT
                )
            """)

            overall_compliance = (compliance_metrics['uk_spelling_compliance'] +
                               compliance_metrics['aud_currency_compliance']) / 2

            cursor.execute("""
                INSERT INTO compliance_reports (
                    uk_spelling_compliance, aud_currency_compliance, overall_compliance, report_json
                ) VALUES (?, ?, ?, ?)
            """, (
                compliance_metrics['uk_spelling_compliance'],
                compliance_metrics['aud_currency_compliance'],
                overall_compliance,
                json.dumps(compliance_metrics)
            ))

            conn.commit()
            conn.close()

        except Exception as e:
            logger.error(f"❌ Failed to store compliance metrics: {e}")

    async def store_system_metrics(self, system_metrics: Dict[str, Any]):
        """Store system performance metrics."""
        self.metrics_history.append(system_metrics)

        # Keep only last 100 metrics
        if len(self.metrics_history) > 100:
            self.metrics_history = self.metrics_history[-100:]

    async def store_alerts(self, alerts: List[Dict[str, Any]]):
        """Store alerts in database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Create alerts table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS monitoring_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    alert_id TEXT UNIQUE NOT NULL,
                    alert_type TEXT,
                    severity TEXT,
                    message TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    source TEXT,
                    details_json TEXT,
                    resolved BOOLEAN DEFAULT FALSE,
                    resolution_time TIMESTAMP
                )
            """)

            for alert in alerts:
                alert_id = f"ALERT_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{alert['type']}"

                cursor.execute("""
                    INSERT INTO monitoring_alerts (
                        alert_id, alert_type, severity, message, source, details_json
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    alert_id,
                    alert['type'],
                    alert['severity'],
                    alert['message'],
                    'monitoring_bot',
                    json.dumps(alert)
                ))

            conn.commit()
            conn.close()

        except Exception as e:
            logger.error(f"❌ Failed to store alerts: {e}")

async def main():
    """Main function to run the monitoring bot."""
    # Create logs directory
    os.makedirs('logs', exist_ok=True)

    # Initialize and start monitoring bot
    bot = MovemberMonitoringBot()
    await bot.start_monitoring()

if __name__ == "__main__":
    asyncio.run(main())
