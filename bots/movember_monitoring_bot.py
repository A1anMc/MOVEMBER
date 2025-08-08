#!/usr/bin/env python3
"""
Movember AI Rules System - Monitoring Bot
Automated monitoring and validation bot with UK spelling and AUD currency standards.
"""

import asyncio
import logging
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import httpx
import aiohttp
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from rules.domains.movember_ai import MovemberAIRulesEngine
from rules.types import ExecutionContext, ContextType, RulePriority

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database setup
engine = create_engine("sqlite:///movember_ai.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@dataclass
class MonitoringAlert:
    """Alert data structure."""
    alert_id: str
    alert_type: str
    severity: str
    message: str
    timestamp: datetime
    source: str
    details: Dict
    resolved: bool = False
    resolution_time: Optional[datetime] = None


@dataclass
class DataQualityReport:
    """Data quality report structure."""
    report_id: str
    timestamp: datetime
    total_records: int
    valid_records: int
    invalid_records: int
    uk_spelling_issues: int
    aud_currency_issues: int
    data_gaps: List[str]
    recommendations: List[str]
    quality_score: float


class MovemberMonitoringBot:
    """Automated monitoring bot for Movember AI Rules System."""

    def __init__(self):
        self.engine = MovemberAIRulesEngine()
        self.db = SessionLocal()
        self.logger = logging.getLogger(__name__)
        self.alerts = []
        self.monitoring_interval = 300  # 5 minutes
        self.health_check_interval = 60  # 1 minute
        self.data_quality_interval = 3600  # 1 hour
        self.is_running = False

        # Monitoring thresholds
        self.thresholds = {
            "success_rate": 0.9,
            "response_time": 2.0,
            "error_rate": 0.05,
            "memory_usage": 80.0,
            "cpu_usage": 80.0,
            "disk_usage": 85.0,
            "uk_spelling_consistency": 0.95,
            "aud_currency_compliance": 0.95
        }

    async def start_monitoring(self):
        """Start the monitoring bot."""
        self.logger.info("Starting Movember Monitoring Bot")
        self.is_running = True

        # Start monitoring tasks
        tasks = [
            asyncio.create_task(self._health_monitoring_loop()),
            asyncio.create_task(self._data_quality_monitoring_loop()),
            asyncio.create_task(self._compliance_monitoring_loop()),
            asyncio.create_task(self._performance_monitoring_loop()),
            asyncio.create_task(self._alert_processing_loop())
        ]

        try:
            await asyncio.gather(*tasks)
        except Exception as e:
            self.logger.error(f"Monitoring bot error: {str(e)}")
            self.is_running = False

    async def stop_monitoring(self):
        """Stop the monitoring bot."""
        self.logger.info("Stopping Movember Monitoring Bot")
        self.is_running = False

    async def _health_monitoring_loop(self):
        """Continuous health monitoring loop."""
        while self.is_running:
            try:
                await self._check_system_health()
                await asyncio.sleep(self.health_check_interval)
            except Exception as e:
                self.logger.error(f"Health monitoring error: {str(e)}")
                await asyncio.sleep(30)  # Wait before retry

    async def _data_quality_monitoring_loop(self):
        """Continuous data quality monitoring loop."""
        while self.is_running:
            try:
                await self._check_data_quality()
                await asyncio.sleep(self.data_quality_interval)
            except Exception as e:
                self.logger.error(f"Data quality monitoring error: {str(e)}")
                await asyncio.sleep(300)  # Wait before retry

    async def _compliance_monitoring_loop(self):
        """Continuous compliance monitoring loop."""
        while self.is_running:
            try:
                await self._check_compliance_standards()
                await asyncio.sleep(self.monitoring_interval)
            except Exception as e:
                self.logger.error(f"Compliance monitoring error: {str(e)}")
                await asyncio.sleep(300)  # Wait before retry

    async def _performance_monitoring_loop(self):
        """Continuous performance monitoring loop."""
        while self.is_running:
            try:
                await self._check_performance_metrics()
                await asyncio.sleep(self.monitoring_interval)
            except Exception as e:
                self.logger.error(f"Performance monitoring error: {str(e)}")
                await asyncio.sleep(300)  # Wait before retry

    async def _alert_processing_loop(self):
        """Process and handle alerts."""
        while self.is_running:
            try:
                await self._process_alerts()
                await asyncio.sleep(60)  # Check alerts every minute
            except Exception as e:
                self.logger.error(f"Alert processing error: {str(e)}")
                await asyncio.sleep(60)  # Wait before retry

    async def _check_system_health(self):
        """Check system health and generate alerts if needed."""
        try:
            # Get system metrics
            metrics = self.engine.get_metrics()
            system_metrics = metrics.get("system_metrics", {})

            # Check success rate
            success_rate = system_metrics.get("success_rate", 1.0)
            if success_rate < self.thresholds["success_rate"]:
                await self._create_alert(
                    alert_type="performance",
                    severity="warning",
                    message=f"System success rate below threshold: {success_rate:.2%}",
                    source="health_monitor",
                    details={"success_rate": success_rate, "threshold": self.thresholds["success_rate"]}
                )

            # Check error rate
            error_rate = 1.0 - success_rate
            if error_rate > self.thresholds["error_rate"]:
                await self._create_alert(
                    alert_type="error",
                    severity="critical",
                    message=f"System error rate above threshold: {error_rate:.2%}",
                    source="health_monitor",
                    details={"error_rate": error_rate, "threshold": self.thresholds["error_rate"]}
                )

            # Check response time
            avg_response_time = system_metrics.get("average_response_time", 0.0)
            if avg_response_time > self.thresholds["response_time"]:
                await self._create_alert(
                    alert_type="performance",
                    severity="warning",
                    message=f"Average response time above threshold: {avg_response_time:.2f}s",
                    source="health_monitor",
                    details={"response_time": avg_response_time, "threshold": self.thresholds["response_time"]}
                )

            self.logger.info("System health check completed successfully")

        except Exception as e:
            self.logger.error(f"Health check error: {str(e)}")
            await self._create_alert(
                alert_type="system",
                severity="critical",
                message=f"Health check failed: {str(e)}",
                source="health_monitor",
                details={"error": str(e)}
            )

    async def _check_data_quality(self):
        """Check data quality and generate report."""
        try:
            # Query database for recent records
            with self.db.begin():
                result = self.db.execute(text("""
                    SELECT COUNT(*) as total_records,
                           SUM(CASE WHEN data_json LIKE '%"currency": "AUD"%' THEN 1 ELSE 0 END) as aud_compliant,
                           SUM(CASE WHEN data_json LIKE '%color%' OR data_json LIKE '%behavior%' THEN 1 ELSE 0 END) as spelling_issues
                    FROM grants
                    WHERE created_at >= :since
                """), {"since": datetime.now() - timedelta(hours=24)})

                row = result.fetchone()
                total_records = row.total_records if row else 0
                aud_compliant = row.aud_compliant if row else 0
                spelling_issues = row.spelling_issues if row else 0

            # Calculate quality metrics
            aud_currency_compliance = aud_compliant / total_records if total_records > 0 else 1.0
            uk_spelling_consistency = 1.0 - (spelling_issues / total_records if total_records > 0 else 0.0)

            # Generate quality report
            report = DataQualityReport(
                report_id=f"DQ-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                timestamp=datetime.now(),
                total_records=total_records,
                valid_records=total_records - spelling_issues,
                invalid_records=spelling_issues,
                uk_spelling_issues=spelling_issues,
                aud_currency_issues=total_records - aud_compliant,
                data_gaps=[],
                recommendations=[],
                quality_score=min(aud_currency_compliance, uk_spelling_consistency)
            )

            # Check compliance thresholds
            if aud_currency_compliance < self.thresholds["aud_currency_compliance"]:
                await self._create_alert(
                    alert_type="compliance",
                    severity="warning",
                    message=f"AUD currency compliance below threshold: {aud_currency_compliance:.2%}",
                    source="data_quality_monitor",
                    details={"compliance": aud_currency_compliance, "threshold": self.thresholds["aud_currency_compliance"]}
                )

            if uk_spelling_consistency < self.thresholds["uk_spelling_consistency"]:
                await self._create_alert(
                    alert_type="compliance",
                    severity="warning",
                    message=f"UK spelling consistency below threshold: {uk_spelling_consistency:.2%}",
                    source="data_quality_monitor",
                    details={"consistency": uk_spelling_consistency, "threshold": self.thresholds["uk_spelling_consistency"]}
                )

            # Store quality report
            await self._store_quality_report(report)

            self.logger.info(f"Data quality check completed: {report.quality_score:.2%} quality score")

        except Exception as e:
            self.logger.error(f"Data quality check error: {str(e)}")
            await self._create_alert(
                alert_type="system",
                severity="critical",
                message=f"Data quality check failed: {str(e)}",
                source="data_quality_monitor",
                details={"error": str(e)}
            )

    async def _check_compliance_standards(self):
        """Check compliance with UK spelling and AUD currency standards."""
        try:
            # Check rule compliance
            rules = self.engine.engine.rules
            uk_spelling_compliant = 0
            aud_currency_compliant = 0

            for rule in rules:
                # Check UK spelling in rule descriptions
                if hasattr(rule, 'description') and rule.description:
                    if not self._contains_american_spelling(rule.description):
                        uk_spelling_compliant += 1

                # Check AUD currency in rule actions
                if hasattr(rule, 'actions') and rule.actions:
                    for action in rule.actions:
                        if hasattr(action, 'parameters') and action.parameters:
                            if 'currency' in str(action.parameters) and 'AUD' in str(action.parameters):
                                aud_currency_compliant += 1

            total_rules = len(rules)
            uk_compliance = uk_spelling_compliant / total_rules if total_rules > 0 else 1.0
            aud_compliance = aud_currency_compliant / total_rules if total_rules > 0 else 1.0

            # Generate compliance report
            compliance_report = {
                "timestamp": datetime.now(),
                "total_rules": total_rules,
                "uk_spelling_compliance": uk_compliance,
                "aud_currency_compliance": aud_compliance,
                "overall_compliance": min(uk_compliance, aud_compliance)
            }

            # Store compliance report
            await self._store_compliance_report(compliance_report)

            self.logger.info(f"Compliance check completed: {compliance_report['overall_compliance']:.2%} compliance")

        except Exception as e:
            self.logger.error(f"Compliance check error: {str(e)}")
            await self._create_alert(
                alert_type="compliance",
                severity="critical",
                message=f"Compliance check failed: {str(e)}",
                source="compliance_monitor",
                details={"error": str(e)}
            )

    async def _check_performance_metrics(self):
        """Check performance metrics and generate alerts if needed."""
        try:
            # Get performance metrics
            metrics = self.engine.get_metrics()
            system_metrics = metrics.get("system_metrics", {})

            # Check execution time
            total_executions = system_metrics.get("total_executions", 0)
            if total_executions > 0:
                avg_execution_time = system_metrics.get("average_execution_time", 0.0)
                if avg_execution_time > self.thresholds["response_time"]:
                    await self._create_alert(
                        alert_type="performance",
                        severity="warning",
                        message=f"Average execution time above threshold: {avg_execution_time:.2f}s",
                        source="performance_monitor",
                        details={"execution_time": avg_execution_time, "threshold": self.thresholds["response_time"]}
                    )

            # Check rule performance
            rule_metrics = metrics.get("rule_metrics", {})
            for rule_name, rule_data in rule_metrics.items():
                success_rate = rule_data.get("success_rate", 1.0)
                if success_rate < self.thresholds["success_rate"]:
                    await self._create_alert(
                        alert_type="rule_performance",
                        severity="warning",
                        message=f"Rule '{rule_name}' success rate below threshold: {success_rate:.2%}",
                        source="performance_monitor",
                        details={"rule": rule_name, "success_rate": success_rate, "threshold": self.thresholds["success_rate"]}
                    )

            self.logger.info("Performance metrics check completed")

        except Exception as e:
            self.logger.error(f"Performance check error: {str(e)}")
            await self._create_alert(
                alert_type="system",
                severity="critical",
                message=f"Performance check failed: {str(e)}",
                source="performance_monitor",
                details={"error": str(e)}
            )

    async def _create_alert(self, alert_type: str, severity: str, message: str, source: str, details: Dict):
        """Create and store an alert."""
        alert = MonitoringAlert(
            alert_id=f"ALERT-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            alert_type=alert_type,
            severity=severity,
            message=message,
            timestamp=datetime.now(),
            source=source,
            details=details
        )

        self.alerts.append(alert)

        # Log alert
        log_level = logging.ERROR if severity == "critical" else logging.WARNING
        self.logger.log(log_level, f"Alert [{severity.upper()}]: {message}")

        # Store alert in database
        await self._store_alert(alert)

        # Send notification if critical
        if severity == "critical":
            await self._send_critical_alert(alert)

    async def _process_alerts(self):
        """Process and resolve alerts."""
        current_time = datetime.now()

        for alert in self.alerts[:]:  # Copy list to avoid modification during iteration
            # Auto-resolve alerts older than 24 hours
            if not alert.resolved and (current_time - alert.timestamp) > timedelta(hours=24):
                alert.resolved = True
                alert.resolution_time = current_time

                # Update database
                await self._update_alert_resolution(alert)

                self.logger.info(f"Auto-resolved alert: {alert.alert_id}")

        # Clean up old alerts (older than 7 days)
        cutoff_time = current_time - timedelta(days=7)
        self.alerts = [alert for alert in self.alerts if alert.timestamp > cutoff_time]

    def _contains_american_spelling(self, text: str) -> bool:
        """Check if text contains American spelling."""
        american_spellings = [
            'color', 'behavior', 'organization', 'realize', 'analyze',
            'center', 'meter', 'program', 'license', 'defense', 'offense',
            'specialize', 'standardize', 'optimize', 'customize', 'summarize',
            'categorize', 'prioritize'
        ]

        text_lower = text.lower()
        return any(spelling in text_lower for spelling in american_spellings)

    async def _store_quality_report(self, report: DataQualityReport):
        """Store data quality report in database."""
        try:
            with self.db.begin():
                self.db.execute(text("""
                    INSERT INTO data_quality_reports (
                        report_id, timestamp, total_records, valid_records, invalid_records,
                        uk_spelling_issues, aud_currency_issues, quality_score, report_json
                    ) VALUES (
                        :report_id, :timestamp, :total_records, :valid_records, :invalid_records,
                        :uk_spelling_issues, :aud_currency_issues, :quality_score, :report_json
                    )
                """), {
                    "report_id": report.report_id,
                    "timestamp": report.timestamp,
                    "total_records": report.total_records,
                    "valid_records": report.valid_records,
                    "invalid_records": report.invalid_records,
                    "uk_spelling_issues": report.uk_spelling_issues,
                    "aud_currency_issues": report.aud_currency_issues,
                    "quality_score": report.quality_score,
                    "report_json": json.dumps(asdict(report))
                })
        except Exception as e:
            self.logger.error(f"Error storing quality report: {str(e)}")

    async def _store_compliance_report(self, report: Dict):
        """Store compliance report in database."""
        try:
            with self.db.begin():
                self.db.execute(text("""
                    INSERT INTO compliance_reports (
                        timestamp, total_rules, uk_spelling_compliance, aud_currency_compliance,
                        overall_compliance, report_json
                    ) VALUES (
                        :timestamp, :total_rules, :uk_spelling_compliance, :aud_currency_compliance,
                        :overall_compliance, :report_json
                    )
                """), {
                    "timestamp": report["timestamp"],
                    "total_rules": report["total_rules"],
                    "uk_spelling_compliance": report["uk_spelling_compliance"],
                    "aud_currency_compliance": report["aud_currency_compliance"],
                    "overall_compliance": report["overall_compliance"],
                    "report_json": json.dumps(report)
                })
        except Exception as e:
            self.logger.error(f"Error storing compliance report: {str(e)}")

    async def _store_alert(self, alert: MonitoringAlert):
        """Store alert in database."""
        try:
            with self.db.begin():
                self.db.execute(text("""
                    INSERT INTO monitoring_alerts (
                        alert_id, alert_type, severity, message, timestamp, source,
                        details_json, resolved, resolution_time
                    ) VALUES (
                        :alert_id, :alert_type, :severity, :message, :timestamp, :source,
                        :details_json, :resolved, :resolution_time
                    )
                """), {
                    "alert_id": alert.alert_id,
                    "alert_type": alert.alert_type,
                    "severity": alert.severity,
                    "message": alert.message,
                    "timestamp": alert.timestamp,
                    "source": alert.source,
                    "details_json": json.dumps(alert.details),
                    "resolved": alert.resolved,
                    "resolution_time": alert.resolution_time
                })
        except Exception as e:
            self.logger.error(f"Error storing alert: {str(e)}")

    async def _update_alert_resolution(self, alert: MonitoringAlert):
        """Update alert resolution status in database."""
        try:
            with self.db.begin():
                self.db.execute(text("""
                    UPDATE monitoring_alerts
                    SET resolved = :resolved, resolution_time = :resolution_time
                    WHERE alert_id = :alert_id
                """), {
                    "resolved": alert.resolved,
                    "resolution_time": alert.resolution_time,
                    "alert_id": alert.alert_id
                })
        except Exception as e:
            self.logger.error(f"Error updating alert resolution: {str(e)}")

    async def _send_critical_alert(self, alert: MonitoringAlert):
        """Send critical alert notification."""
        try:
            # Implementation for sending notifications (email, Slack, etc.)
            notification_message = f"""
🚨 CRITICAL ALERT - Movember AI Rules System

Alert ID: {alert.alert_id}
Type: {alert.alert_type}
Severity: {alert.severity}
Message: {alert.message}
Source: {alert.source}
Timestamp: {alert.timestamp}

Details: {json.dumps(alert.details, indent=2)}

Please investigate immediately.
            """

            # Log notification (replace with actual notification service)
            self.logger.critical(notification_message)

        except Exception as e:
            self.logger.error(f"Error sending critical alert: {str(e)}")

    def get_alerts(self, severity: Optional[str] = None, resolved: Optional[bool] = None) -> List[MonitoringAlert]:
        """Get alerts with optional filtering."""
        alerts = self.alerts

        if severity:
            alerts = [alert for alert in alerts if alert.severity == severity]

        if resolved is not None:
            alerts = [alert for alert in alerts if alert.resolved == resolved]

        return alerts

    def get_quality_reports(self, hours: int = 24) -> List[DataQualityReport]:
        """Get recent data quality reports."""
        # Implementation for retrieving quality reports from database
        return []

    def get_compliance_reports(self, hours: int = 24) -> List[Dict]:
        """Get recent compliance reports."""
        # Implementation for retrieving compliance reports from database
        return []


async def main():
    """Main function to run the monitoring bot."""
    bot = MovemberMonitoringBot()

    try:
        await bot.start_monitoring()
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
        await bot.stop_monitoring()
    except Exception as e:
        logger.error(f"Bot error: {str(e)}")
        await bot.stop_monitoring()


if __name__ == "__main__":
    asyncio.run(main())
