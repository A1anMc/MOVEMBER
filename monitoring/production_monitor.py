#!/usr/bin/env python3
"""
Production Monitoring System for Movember AI Rules System
Comprehensive monitoring, alerting, and performance tracking.
"""

import asyncio
import json
import logging
import time
import psutil
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import aiohttp
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlertLevel(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class MetricType(Enum):
    """Types of metrics to monitor."""
    SYSTEM = "system"
    APPLICATION = "application"
    DATABASE = "database"
    API = "api"
    SECURITY = "security"

@dataclass
class Alert:
    """Alert notification."""
    alert_id: str
    level: AlertLevel
    title: str
    message: str
    timestamp: datetime
    metric_type: MetricType
    value: float
    threshold: float
    resolved: bool = False
    resolved_at: Optional[datetime] = None

@dataclass
class Metric:
    """Performance metric."""
    metric_id: str
    name: str
    value: float
    unit: str
    metric_type: MetricType
    timestamp: datetime
    tags: Dict[str, str]

@dataclass
class SystemHealth:
    """System health status."""
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_io: Dict[str, float]
    uptime: float
    active_connections: int
    timestamp: datetime

class ProductionMonitor:
    """Production monitoring system for Movember AI Rules System."""

    def __init__(self, db_path: str = "monitoring.db", alert_email: Optional[str] = None):
        self.db_path = db_path
        self.alert_email = alert_email
        self.metrics: List[Metric] = []
        self.alerts: List[Alert] = []
        self.thresholds = {
            "cpu_usage": 80.0,
            "memory_usage": 85.0,
            "disk_usage": 90.0,
            "response_time": 2.0,
            "error_rate": 5.0,
            "uptime": 99.5
        }
        self.init_database()
        self.monitoring_active = False
        logger.info("Production Monitor initialized")

    def init_database(self):
        """Initialize monitoring database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_id TEXT UNIQUE,
                name TEXT NOT NULL,
                value REAL NOT NULL,
                unit TEXT NOT NULL,
                metric_type TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                tags TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alert_id TEXT UNIQUE,
                level TEXT NOT NULL,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                metric_type TEXT NOT NULL,
                value REAL NOT NULL,
                threshold REAL NOT NULL,
                resolved BOOLEAN DEFAULT FALSE,
                resolved_at TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create system_health table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_health (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cpu_usage REAL NOT NULL,
                memory_usage REAL NOT NULL,
                disk_usage REAL NOT NULL,
                network_io TEXT,
                uptime REAL NOT NULL,
                active_connections INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()
        logger.info("Monitoring database initialized")

    async def start_monitoring(self):
        """Start the monitoring system."""
        self.monitoring_active = True
        logger.info("Production monitoring started")
        
        while self.monitoring_active:
            try:
                # Collect system metrics
                await self.collect_system_metrics()
                
                # Collect application metrics
                await self.collect_application_metrics()
                
                # Collect database metrics
                await self.collect_database_metrics()
                
                # Collect API metrics
                await self.collect_api_metrics()
                
                # Check thresholds and generate alerts
                await self.check_thresholds()
                
                # Store metrics in database
                await self.store_metrics()
                
                # Wait before next collection
                await asyncio.sleep(30)  # Collect every 30 seconds
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(60)  # Wait longer on error

    async def collect_system_metrics(self):
        """Collect system-level metrics."""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            self.add_metric("cpu_usage", cpu_percent, "%", MetricType.SYSTEM)
            
            # Memory usage
            memory = psutil.virtual_memory()
            self.add_metric("memory_usage", memory.percent, "%", MetricType.SYSTEM)
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            self.add_metric("disk_usage", disk_percent, "%", MetricType.SYSTEM)
            
            # Network I/O
            network = psutil.net_io_counters()
            self.add_metric("network_bytes_sent", network.bytes_sent, "bytes", MetricType.SYSTEM)
            self.add_metric("network_bytes_recv", network.bytes_recv, "bytes", MetricType.SYSTEM)
            
            # Uptime
            uptime = time.time() - psutil.boot_time()
            self.add_metric("system_uptime", uptime / 3600, "hours", MetricType.SYSTEM)
            
            logger.debug("System metrics collected")
            
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")

    async def collect_application_metrics(self):
        """Collect application-level metrics."""
        try:
            # Get current process info
            process = psutil.Process()
            
            # Process CPU usage
            process_cpu = process.cpu_percent()
            self.add_metric("process_cpu_usage", process_cpu, "%", MetricType.APPLICATION)
            
            # Process memory usage
            process_memory = process.memory_info().rss / 1024 / 1024  # MB
            self.add_metric("process_memory_usage", process_memory, "MB", MetricType.APPLICATION)
            
            # Process uptime
            process_uptime = time.time() - process.create_time()
            self.add_metric("process_uptime", process_uptime / 3600, "hours", MetricType.APPLICATION)
            
            # Active threads
            thread_count = process.num_threads()
            self.add_metric("active_threads", thread_count, "count", MetricType.APPLICATION)
            
            logger.debug("Application metrics collected")
            
        except Exception as e:
            logger.error(f"Error collecting application metrics: {e}")

    async def collect_database_metrics(self):
        """Collect database performance metrics."""
        try:
            # Check database connection
            start_time = time.time()
            conn = sqlite3.connect("movember_ai.db")
            cursor = conn.cursor()
            
            # Test query performance
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
            result = cursor.fetchone()
            query_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            self.add_metric("database_query_time", query_time, "ms", MetricType.DATABASE)
            self.add_metric("database_tables", result[0], "count", MetricType.DATABASE)
            
            # Check database size
            cursor.execute("PRAGMA page_count")
            page_count = cursor.fetchone()[0]
            cursor.execute("PRAGMA page_size")
            page_size = cursor.fetchone()[0]
            db_size = (page_count * page_size) / 1024 / 1024  # MB
            self.add_metric("database_size", db_size, "MB", MetricType.DATABASE)
            
            conn.close()
            logger.debug("Database metrics collected")
            
        except Exception as e:
            logger.error(f"Error collecting database metrics: {e}")

    async def collect_api_metrics(self):
        """Collect API performance metrics."""
        try:
            # Test API health endpoint
            start_time = time.time()
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get('http://localhost:8000/health/') as response:
                        response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
                        status_code = response.status
                        
                        self.add_metric("api_response_time", response_time, "ms", MetricType.API)
                        self.add_metric("api_status_code", status_code, "code", MetricType.API)
                        
                        if status_code == 200:
                            self.add_metric("api_health", 1, "status", MetricType.API)
                        else:
                            self.add_metric("api_health", 0, "status", MetricType.API)
                            
                except Exception as e:
                    self.add_metric("api_health", 0, "status", MetricType.API)
                    self.add_metric("api_response_time", 9999, "ms", MetricType.API)
                    logger.warning(f"API health check failed: {e}")
            
            logger.debug("API metrics collected")
            
        except Exception as e:
            logger.error(f"Error collecting API metrics: {e}")

    def add_metric(self, name: str, value: float, unit: str, metric_type: MetricType, tags: Optional[Dict[str, str]] = None):
        """Add a new metric."""
        metric_id = f"{metric_type.value}_{name}_{int(time.time())}"
        metric = Metric(
            metric_id=metric_id,
            name=name,
            value=value,
            unit=unit,
            metric_type=metric_type,
            timestamp=datetime.now(),
            tags=tags or {}
        )
        self.metrics.append(metric)

    async def check_thresholds(self):
        """Check metrics against thresholds and generate alerts."""
        for metric in self.metrics[-100:]:  # Check last 100 metrics
            threshold = self.thresholds.get(metric.name)
            if threshold is not None:
                if metric.value > threshold:
                    await self.create_alert(
                        level=AlertLevel.WARNING if metric.value < threshold * 1.5 else AlertLevel.ERROR,
                        title=f"High {metric.name}",
                        message=f"{metric.name} is {metric.value}{metric.unit} (threshold: {threshold}{metric.unit})",
                        metric_type=metric.metric_type,
                        value=metric.value,
                        threshold=threshold
                    )

    async def create_alert(self, level: AlertLevel, title: str, message: str, 
                          metric_type: MetricType, value: float, threshold: float):
        """Create a new alert."""
        alert_id = f"alert_{int(time.time())}_{level.value}"
        alert = Alert(
            alert_id=alert_id,
            level=level,
            title=title,
            message=message,
            timestamp=datetime.now(),
            metric_type=metric_type,
            value=value,
            threshold=threshold
        )
        
        self.alerts.append(alert)
        logger.warning(f"Alert created: {title} - {message}")
        
        # Send email alert if configured
        if self.alert_email and level in [AlertLevel.ERROR, AlertLevel.CRITICAL]:
            await self.send_email_alert(alert)

    async def send_email_alert(self, alert: Alert):
        """Send email alert."""
        try:
            # This is a placeholder - you would configure with your email service
            logger.info(f"Email alert would be sent: {alert.title}")
        except Exception as e:
            logger.error(f"Error sending email alert: {e}")

    async def store_metrics(self):
        """Store metrics in database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Store metrics
            for metric in self.metrics[-50:]:  # Store last 50 metrics
                cursor.execute('''
                    INSERT OR REPLACE INTO metrics 
                    (metric_id, name, value, unit, metric_type, timestamp, tags)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    metric.metric_id,
                    metric.name,
                    metric.value,
                    metric.unit,
                    metric.metric_type.value,
                    metric.timestamp.isoformat(),
                    json.dumps(metric.tags)
                ))
            
            # Store alerts
            for alert in self.alerts[-20:]:  # Store last 20 alerts
                cursor.execute('''
                    INSERT OR REPLACE INTO alerts 
                    (alert_id, level, title, message, timestamp, metric_type, value, threshold, resolved, resolved_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    alert.alert_id,
                    alert.level.value,
                    alert.title,
                    alert.message,
                    alert.timestamp.isoformat(),
                    alert.metric_type.value,
                    alert.value,
                    alert.threshold,
                    alert.resolved,
                    alert.resolved_at.isoformat() if alert.resolved_at else None
                ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error storing metrics: {e}")

    def get_system_health(self) -> SystemHealth:
        """Get current system health status."""
        try:
            cpu_usage = psutil.cpu_percent()
            memory_usage = psutil.virtual_memory().percent
            disk_usage = (psutil.disk_usage('/').used / psutil.disk_usage('/').total) * 100
            network = psutil.net_io_counters()
            uptime = time.time() - psutil.boot_time()
            
            return SystemHealth(
                cpu_usage=cpu_usage,
                memory_usage=memory_usage,
                disk_usage=disk_usage,
                network_io={
                    "bytes_sent": network.bytes_sent,
                    "bytes_recv": network.bytes_recv
                },
                uptime=uptime,
                active_connections=len(psutil.net_connections()),
                timestamp=datetime.now()
            )
        except Exception as e:
            logger.error(f"Error getting system health: {e}")
            return SystemHealth(
                cpu_usage=0.0,
                memory_usage=0.0,
                disk_usage=0.0,
                network_io={"bytes_sent": 0, "bytes_recv": 0},
                uptime=0.0,
                active_connections=0,
                timestamp=datetime.now()
            )

    def get_recent_metrics(self, metric_type: Optional[MetricType] = None, limit: int = 100) -> List[Metric]:
        """Get recent metrics from database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if metric_type:
                cursor.execute('''
                    SELECT metric_id, name, value, unit, metric_type, timestamp, tags
                    FROM metrics 
                    WHERE metric_type = ?
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (metric_type.value, limit))
            else:
                cursor.execute('''
                    SELECT metric_id, name, value, unit, metric_type, timestamp, tags
                    FROM metrics 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (limit,))
            
            results = cursor.fetchall()
            conn.close()
            
            metrics = []
            for row in results:
                metric = Metric(
                    metric_id=row[0],
                    name=row[1],
                    value=row[2],
                    unit=row[3],
                    metric_type=MetricType(row[4]),
                    timestamp=datetime.fromisoformat(row[5]),
                    tags=json.loads(row[6]) if row[6] else {}
                )
                metrics.append(metric)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error getting recent metrics: {e}")
            return []

    def get_active_alerts(self) -> List[Alert]:
        """Get active (unresolved) alerts."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT alert_id, level, title, message, timestamp, metric_type, value, threshold, resolved, resolved_at
                FROM alerts 
                WHERE resolved = FALSE
                ORDER BY timestamp DESC
            ''')
            
            results = cursor.fetchall()
            conn.close()
            
            alerts = []
            for row in results:
                alert = Alert(
                    alert_id=row[0],
                    level=AlertLevel(row[1]),
                    title=row[2],
                    message=row[3],
                    timestamp=datetime.fromisoformat(row[4]),
                    metric_type=MetricType(row[5]),
                    value=row[6],
                    threshold=row[7],
                    resolved=row[8],
                    resolved_at=datetime.fromisoformat(row[9]) if row[9] else None
                )
                alerts.append(alert)
            
            return alerts
            
        except Exception as e:
            logger.error(f"Error getting active alerts: {e}")
            return []

    def stop_monitoring(self):
        """Stop the monitoring system."""
        self.monitoring_active = False
        logger.info("Production monitoring stopped")

# Global monitor instance
production_monitor = ProductionMonitor()

async def start_production_monitoring():
    """Start production monitoring."""
    await production_monitor.start_monitoring()

if __name__ == "__main__":
    # Run monitoring
    asyncio.run(start_production_monitoring())
