#!/usr/bin/env python3
"""
Automated Monitoring and Alerting System for Movember AI Rules System
Monitors system health, performance, and generates alerts for critical issues.
"""

import asyncio
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import httpx
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('monitoring/alerts.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MovemberSystemMonitor:


    """Comprehensive monitoring system for Movember AI Rules System."""

    def __init__(self, api_base_url: str = "https://movember-api.onrender.com"):


        self.api_base_url = api_base_url
        self.alert_history: List[Dict] = []
        self.performance_metrics: Dict[str, List] = {
            'response_times': [],
            'error_rates': [],
            'rule_executions': [],
            'system_health': []
        }
        self.thresholds = {
            'response_time_max': 5.0,  # seconds
            'error_rate_max': 0.1,     # 10%
            'memory_usage_max': 0.8,   # 80%
            'cpu_usage_max': 0.7,      # 70%
            'uptime_min': 0.95,        # 95%
            'rule_execution_min': 1     # at least 1 rule execution per check
        }

    async def check_system_health(self) -> Dict[str, Any]:
        """Check overall system health."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.api_base_url}/health/")
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {"error": str(e)}

    async def check_performance_metrics(self) -> Dict[str, Any]:
        """Check system performance metrics."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.api_base_url}/metrics/")
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Metrics check failed: {e}")
            return {"error": str(e)}

    async def test_scraper_functionality(self) -> Dict[str, Any]:
        """Test scraper functionality."""
        try:
            test_data = {
                "target_url": "https://httpbin.org/html",
                "selectors": {"title": "h1"},
                "data_mapping": {"title": "title"},
                "rate_limit": 1
            }

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.api_base_url}/scraper/",
                    json=test_data,
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Scraper test failed: {e}")
            return {"error": str(e)}

    async def test_rules_engine(self) -> Dict[str, Any]:
        """Test rules engine with sample grant data."""
        try:
            test_grant = {
                "grant_id": "TEST-2024-001",
                "title": "Test Mental Health Program",
                "description": "Test program for monitoring",
                "amount": 25000,
                "budget": 25000,
                "timeline_months": 6,
                "category": "mental_health",
                "target_demographic": "young_men",
                "location": "Victoria",
                "organisation": "Test Organisation",
                "contact_person": "Test Contact",
                "email": "test@example.com",
                "submission_date": datetime.now().strftime("%Y-%m-%d")
            }

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.api_base_url}/grants/",
                    json=test_grant,
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Rules engine test failed: {e}")
            return {"error": str(e)}

    def analyze_health_data(self, health_data: Dict[str, Any]) -> List[Dict[str, Any]]:


        """Analyze health data and generate alerts."""
        alerts = []

        if "error" in health_data:
            alerts.append({
                "level": "CRITICAL",
                "message": f"System health check failed: {health_data['error']}",
                "timestamp": datetime.now().isoformat(),
                "component": "health_check"
            })
            return alerts

        # Check uptime
        uptime = health_data.get('uptime_percentage', 0)
        if uptime < self.thresholds['uptime_min'] * 100:
            alerts.append({
                "level": "WARNING",
                "message": f"Low uptime: {uptime}% (threshold: {self.thresholds['uptime_min'] * 100}%)",
                "timestamp": datetime.now().isoformat(),
                "component": "uptime"
            })

        # Check memory usage
        memory_usage = health_data.get('memory_usage', 0) / 100
        if memory_usage > self.thresholds['memory_usage_max']:
            alerts.append({
                "level": "WARNING",
                "message": f"High memory usage: {memory_usage * 100}% (
                    threshold: {self.thresholds['memory_usage_max'] * 100}%)",
                "timestamp": datetime.now().isoformat(),
                "component": "memory"
            })

        # Check CPU usage
        cpu_usage = health_data.get('cpu_usage', 0) / 100
        if cpu_usage > self.thresholds['cpu_usage_max']:
            alerts.append({
                "level": "WARNING",
                "message": f"High CPU usage: {cpu_usage * 100}% (threshold: {self.thresholds['cpu_usage_max'] * 100}%)",
                "timestamp": datetime.now().isoformat(),
                "component": "cpu"
            })

        # Check active rules
        active_rules = health_data.get('active_rules', 0)
        if active_rules < 70:  # Should have at least 70 rules active
            alerts.append({
                "level": "WARNING",
                "message": f"Low number of active rules: {active_rules} (expected: 70+)",
                "timestamp": datetime.now().isoformat(),
                "component": "rules_engine"
            })

        return alerts

    def analyze_performance_data(self, metrics_data: Dict[str, Any]) -> List[Dict[str, Any]]:


        """Analyze performance metrics and generate alerts."""
        alerts = []

        if "error" in metrics_data:
            alerts.append({
                "level": "CRITICAL",
                "message": f"Performance metrics check failed: {metrics_data['error']}",
                "timestamp": datetime.now().isoformat(),
                "component": "metrics"
            })
            return alerts

        metrics = metrics_data.get('metrics', {}).get('system_metrics', {})

        # Check average response time
        avg_response_time = metrics.get('average_batch_time', 0)
        if avg_response_time > self.thresholds['response_time_max']:
            alerts.append({
                "level": "WARNING",
                "message": f"Slow response time: {avg_response_time}s (
                    threshold: {self.thresholds['response_time_max']}s)",
                "timestamp": datetime.now().isoformat(),
                "component": "performance"
            })

        # Check success rate
        success_rate = metrics.get('success_rate', 1.0)
        error_rate = 1.0 - success_rate
        if error_rate > self.thresholds['error_rate_max']:
            alerts.append({
                "level": "CRITICAL",
                "message": f"High error rate: {error_rate * 100}% (
                    threshold: {self.thresholds['error_rate_max'] * 100}%)",
                "timestamp": datetime.now().isoformat(),
                "component": "reliability"
            })

        # Check total executions
        total_executions = metrics.get('total_executions', 0)
        if total_executions < self.thresholds['rule_execution_min']:
            alerts.append({
                "level": "INFO",
                "message": f"Low activity: {total_executions} total executions",
                "timestamp": datetime.now().isoformat(),
                "component": "activity"
            })

        return alerts

    def send_email_alert(self, alert: Dict[str, Any]) -> bool:


        """Send email alert (placeholder for email configuration)."""
        try:
            # This is a placeholder - in production you'd configure SMTP
            logger.info(f"EMAIL ALERT [{alert['level']}]: {alert['message']}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")
            return False

    def log_alert(self, alert: Dict[str, Any]) -> None:


        """Log alert to file and console."""
        alert_str = f"[{alert['level']}] {alert['component']}: {alert['message']}"
        logger.warning(alert_str)

        # Store in alert history
        self.alert_history.append(alert)

        # Keep only last 100 alerts
        if len(self.alert_history) > 100:
            self.alert_history = self.alert_history[-100:]

    async def run_monitoring_cycle(self) -> Dict[str, Any]:
        """Run a complete monitoring cycle."""
        start_time = time.time()
        cycle_results = {
            "timestamp": datetime.now().isoformat(),
            "health_status": "unknown",
            "performance_status": "unknown",
            "scraper_status": "unknown",
            "rules_engine_status": "unknown",
            "alerts_generated": 0,
            "cycle_duration": 0
        }

        try:
            # 1. Check system health
            logger.info("Starting monitoring cycle...")
            health_data = await self.check_system_health()
            health_alerts = self.analyze_health_data(health_data)

            if "error" not in health_data:
                cycle_results["health_status"] = "healthy"
            else:
                cycle_results["health_status"] = "unhealthy"

            # 2. Check performance metrics
            metrics_data = await self.check_performance_metrics()
            performance_alerts = self.analyze_performance_data(metrics_data)

            if "error" not in metrics_data:
                cycle_results["performance_status"] = "healthy"
            else:
                cycle_results["performance_status"] = "unhealthy"

            # 3. Test scraper functionality
            scraper_data = await self.test_scraper_functionality()
            if "error" not in scraper_data:
                cycle_results["scraper_status"] = "healthy"
            else:
                cycle_results["scraper_status"] = "unhealthy"

            # 4. Test rules engine
            rules_data = await self.test_rules_engine()
            if "error" not in rules_data:
                cycle_results["rules_engine_status"] = "healthy"
            else:
                cycle_results["rules_engine_status"] = "unhealthy"

            # 5. Process all alerts
            all_alerts = health_alerts + performance_alerts
            for alert in all_alerts:
                self.log_alert(alert)
                if alert["level"] in ["CRITICAL", "WARNING"]:
                    self.send_email_alert(alert)

            cycle_results["alerts_generated"] = len(all_alerts)
            cycle_results["cycle_duration"] = time.time() - start_time

            logger.info(f"Monitoring cycle completed in {cycle_results['cycle_duration']:.2f}s")
            logger.info(f"Generated {len(all_alerts)} alerts")

        except Exception as e:
            logger.error(f"Monitoring cycle failed: {e}")
            cycle_results["error"] = str(e)

        return cycle_results

    async def start_continuous_monitoring(self, interval_seconds: int = 300) -> None:
        """Start continuous monitoring with specified interval."""
        logger.info(f"Starting continuous monitoring with {interval_seconds}s intervals")

        while True:
            try:
                await self.run_monitoring_cycle()
                await asyncio.sleep(interval_seconds)
            except KeyboardInterrupt:
                logger.info("Monitoring stopped by user")
                break
            except Exception as e:
                logger.error(f"Monitoring cycle error: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying

async def main():
    """Main function to run the monitoring system."""
    monitor = MovemberSystemMonitor()

    # Run a single monitoring cycle
    results = await monitor.run_monitoring_cycle()

    # Print results
    print("\n" + "="*60)
    print("MOVEMBER AI RULES SYSTEM - MONITORING REPORT")
    print("="*60)
    print(f"Timestamp: {results['timestamp']}")
    print(f"Health Status: {results['health_status']}")
    print(f"Performance Status: {results['performance_status']}")
    print(f"Scraper Status: {results['scraper_status']}")
    print(f"Rules Engine Status: {results['rules_engine_status']}")
    print(f"Alerts Generated: {results['alerts_generated']}")
    print(f"Cycle Duration: {results['cycle_duration']:.2f}s")
    print("="*60)

    # Print recent alerts
    if monitor.alert_history:
        print("\nRECENT ALERTS:")
        for alert in monitor.alert_history[-5:]:  # Last 5 alerts
            print(f"[{alert['level']}] {alert['component']}: {alert['message']}")

    print("\nMonitoring system ready for continuous operation.")
    print("Use Ctrl+C to stop continuous monitoring.")

if __name__ == "__main__":
    asyncio.run(main())
