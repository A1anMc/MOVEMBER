#!/usr/bin/env python3
"""
Advanced Metrics Dashboard for Movember AI Rules System
Real-time performance monitoring and analytics
"""

import asyncio
import time
import psutil
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import logging
import json
from collections import defaultdict, deque

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetric:
    """Performance metric data structure."""
    timestamp: datetime
    metric_name: str
    value: float
    unit: str
    category: str
    context: Dict[str, Any] = None

@dataclass
class SystemHealth:
    """System health status."""
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_io: Dict[str, float]
    uptime: timedelta
    active_connections: int
    error_rate: float
    response_time_avg: float

class AdvancedMetricsCollector:
    """Advanced metrics collection and analysis."""
    
    def __init__(self, db_path: str = "metrics.db"):
        self.db_path = db_path
        self.metrics_buffer = deque(maxlen=1000)
        self.performance_history = defaultdict(list)
        self.alert_thresholds = {
            "cpu_usage": 80.0,
            "memory_usage": 85.0,
            "disk_usage": 90.0,
            "error_rate": 5.0,
            "response_time_avg": 1000.0  # ms
        }
        self.init_database()
        
    def init_database(self):
        """Initialize metrics database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metric_name TEXT NOT NULL,
                value REAL NOT NULL,
                unit TEXT NOT NULL,
                category TEXT NOT NULL,
                context TEXT
            )
        ''')
        
        # Create index separately
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_performance_metrics 
            ON performance_metrics(timestamp, metric_name, category)
        ''')
        
        # Create system health table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_health (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                cpu_usage REAL,
                memory_usage REAL,
                disk_usage REAL,
                network_io_rx REAL,
                network_io_tx REAL,
                uptime_seconds REAL,
                active_connections INTEGER,
                error_rate REAL,
                response_time_avg REAL
            )
        ''')
        
        # Create alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                alert_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                message TEXT NOT NULL,
                metric_name TEXT,
                metric_value REAL,
                threshold REAL,
                resolved BOOLEAN DEFAULT FALSE
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Advanced metrics database initialized")
    
    async def collect_system_metrics(self) -> SystemHealth:
        """Collect comprehensive system metrics."""
        try:
            # CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_usage = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_usage = (disk.used / disk.total) * 100
            
            # Network I/O
            network = psutil.net_io_counters()
            network_io = {
                "bytes_sent": network.bytes_sent,
                "bytes_recv": network.bytes_recv,
                "packets_sent": network.packets_sent,
                "packets_recv": network.packets_recv
            }
            
            # Uptime
            uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
            
            # Active connections (estimate)
            try:
                active_connections = len(psutil.net_connections())
            except (psutil.AccessDenied, PermissionError):
                active_connections = 0
            
            # Error rate and response time (from buffer)
            error_rate = self._calculate_error_rate()
            response_time_avg = self._calculate_avg_response_time()
            
            health = SystemHealth(
                cpu_usage=cpu_usage,
                memory_usage=memory_usage,
                disk_usage=disk_usage,
                network_io=network_io,
                uptime=uptime,
                active_connections=active_connections,
                error_rate=error_rate,
                response_time_avg=response_time_avg
            )
            
            # Store in database
            await self._store_system_health(health)
            
            # Check for alerts
            await self._check_alerts(health)
            
            return health
            
        except Exception as e:
            logger.error(f"Error collecting system metrics: {str(e)}")
            raise
    
    async def record_performance_metric(self, metric: PerformanceMetric):
        """Record a performance metric."""
        self.metrics_buffer.append(metric)
        self.performance_history[metric.category].append(metric)
        
        # Store in database
        await self._store_metric(metric)
        
        # Keep only recent history (last 24 hours)
        cutoff_time = datetime.now() - timedelta(hours=24)
        self.performance_history[metric.category] = [
            m for m in self.performance_history[metric.category]
            if m.timestamp > cutoff_time
        ]
    
    async def get_performance_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get performance summary for the specified time period."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        # Get metrics from database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT metric_name, AVG(value), MIN(value), MAX(value), COUNT(*)
            FROM performance_metrics
            WHERE timestamp >= ?
            GROUP BY metric_name
        ''', (cutoff_time.isoformat(),))
        
        metrics_summary = {}
        for row in cursor.fetchall():
            metric_name, avg_val, min_val, max_val, count = row
            metrics_summary[metric_name] = {
                "average": avg_val,
                "minimum": min_val,
                "maximum": max_val,
                "count": count
            }
        
        # Get system health summary
        cursor.execute('''
            SELECT 
                AVG(cpu_usage), AVG(memory_usage), AVG(disk_usage),
                AVG(error_rate), AVG(response_time_avg),
                COUNT(*) as total_records
            FROM system_health
            WHERE timestamp >= ?
        ''', (cutoff_time.isoformat(),))
        
        health_row = cursor.fetchone()
        if health_row:
            health_summary = {
                "cpu_usage_avg": health_row[0],
                "memory_usage_avg": health_row[1],
                "disk_usage_avg": health_row[2],
                "error_rate_avg": health_row[3],
                "response_time_avg": health_row[4],
                "total_records": health_row[5]
            }
        else:
            health_summary = {}
        
        conn.close()
        
        return {
            "period_hours": hours,
            "metrics_summary": metrics_summary,
            "health_summary": health_summary,
            "current_alerts": await self._get_active_alerts()
        }
    
    async def get_real_time_metrics(self) -> Dict[str, Any]:
        """Get real-time metrics for dashboard."""
        current_health = await self.collect_system_metrics()
        
        # Get recent performance metrics
        recent_metrics = {}
        for category, metrics in self.performance_history.items():
            if metrics:
                recent_metrics[category] = {
                    "latest_value": metrics[-1].value,
                    "latest_timestamp": metrics[-1].timestamp.isoformat(),
                    "trend": self._calculate_trend(metrics[-10:]) if len(metrics) >= 10 else "stable"
                }
        
        return {
            "system_health": {
                "cpu_usage": current_health.cpu_usage,
                "memory_usage": current_health.memory_usage,
                "disk_usage": current_health.disk_usage,
                "uptime_seconds": current_health.uptime.total_seconds(),
                "active_connections": current_health.active_connections,
                "error_rate": current_health.error_rate,
                "response_time_avg": current_health.response_time_avg
            },
            "recent_metrics": recent_metrics,
            "alerts": await self._get_active_alerts(),
            "timestamp": datetime.now().isoformat()
        }
    
    def _calculate_error_rate(self) -> float:
        """Calculate current error rate from metrics buffer."""
        if not self.metrics_buffer:
            return 0.0
        
        error_metrics = [m for m in self.metrics_buffer if "error" in m.metric_name.lower()]
        total_metrics = len(self.metrics_buffer)
        
        return (len(error_metrics) / total_metrics) * 100 if total_metrics > 0 else 0.0
    
    def _calculate_avg_response_time(self) -> float:
        """Calculate average response time from metrics buffer."""
        response_metrics = [m for m in self.metrics_buffer if "response_time" in m.metric_name.lower()]
        
        if not response_metrics:
            return 0.0
        
        return sum(m.value for m in response_metrics) / len(response_metrics)
    
    def _calculate_trend(self, metrics: List[PerformanceMetric]) -> str:
        """Calculate trend from recent metrics."""
        if len(metrics) < 2:
            return "stable"
        
        values = [m.value for m in metrics]
        first_half = values[:len(values)//2]
        second_half = values[len(values)//2:]
        
        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)
        
        change_percent = ((second_avg - first_avg) / first_avg) * 100 if first_avg > 0 else 0
        
        if change_percent > 10:
            return "increasing"
        elif change_percent < -10:
            return "decreasing"
        else:
            return "stable"
    
    async def _store_metric(self, metric: PerformanceMetric):
        """Store metric in database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO performance_metrics (timestamp, metric_name, value, unit, category, context)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            metric.timestamp.isoformat(),
            metric.metric_name,
            metric.value,
            metric.unit,
            metric.category,
            json.dumps(metric.context) if metric.context else None
        ))
        
        conn.commit()
        conn.close()
    
    async def _store_system_health(self, health: SystemHealth):
        """Store system health in database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO system_health (
                timestamp, cpu_usage, memory_usage, disk_usage,
                network_io_rx, network_io_tx, uptime_seconds,
                active_connections, error_rate, response_time_avg
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            health.cpu_usage,
            health.memory_usage,
            health.disk_usage,
            health.network_io.get("bytes_recv", 0),
            health.network_io.get("bytes_sent", 0),
            health.uptime.total_seconds(),
            health.active_connections,
            health.error_rate,
            health.response_time_avg
        ))
        
        conn.commit()
        conn.close()
    
    async def _check_alerts(self, health: SystemHealth):
        """Check for alert conditions."""
        alerts = []
        
        if health.cpu_usage > self.alert_thresholds["cpu_usage"]:
            alerts.append(("high_cpu", "warning", f"CPU usage is {health.cpu_usage:.1f}%"))
        
        if health.memory_usage > self.alert_thresholds["memory_usage"]:
            alerts.append(("high_memory", "warning", f"Memory usage is {health.memory_usage:.1f}%"))
        
        if health.disk_usage > self.alert_thresholds["disk_usage"]:
            alerts.append(("high_disk", "critical", f"Disk usage is {health.disk_usage:.1f}%"))
        
        if health.error_rate > self.alert_thresholds["error_rate"]:
            alerts.append(("high_error_rate", "critical", f"Error rate is {health.error_rate:.1f}%"))
        
        if health.response_time_avg > self.alert_thresholds["response_time_avg"]:
            alerts.append(("slow_response", "warning", f"Average response time is {health.response_time_avg:.1f}ms"))
        
        # Store alerts
        for alert_type, severity, message in alerts:
            await self._store_alert(alert_type, severity, message)
    
    async def _store_alert(self, alert_type: str, severity: str, message: str):
        """Store alert in database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO alerts (timestamp, alert_type, severity, message)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now().isoformat(), alert_type, severity, message))
        
        conn.commit()
        conn.close()
        
        logger.warning(f"ALERT [{severity.upper()}]: {message}")
    
    async def _get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get active (unresolved) alerts."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT alert_type, severity, message, timestamp
            FROM alerts
            WHERE resolved = FALSE
            ORDER BY timestamp DESC
            LIMIT 10
        ''')
        
        alerts = []
        for row in cursor.fetchall():
            alerts.append({
                "type": row[0],
                "severity": row[1],
                "message": row[2],
                "timestamp": row[3]
            })
        
        conn.close()
        return alerts

# Global metrics collector
_metrics_collector: Optional[AdvancedMetricsCollector] = None

def get_metrics_collector() -> AdvancedMetricsCollector:
    """Get global metrics collector instance."""
    global _metrics_collector
    if _metrics_collector is None:
        _metrics_collector = AdvancedMetricsCollector()
    return _metrics_collector 