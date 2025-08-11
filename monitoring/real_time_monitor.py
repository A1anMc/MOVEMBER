#!/usr/bin/env python3
"""
Real-time Monitoring System
Comprehensive monitoring and alerting for the Movember AI Rules System.
"""

import asyncio
import logging
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import aiohttp
import psutil
import sqlite3
from pathlib import Path

logger = logging.getLogger(__name__)

class AlertLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class MetricType(Enum):
    SYSTEM = "system"
    API = "api"
    DATA = "data"
    PERFORMANCE = "performance"
    BUSINESS = "business"

@dataclass
class Metric:
    """Represents a system metric."""
    name: str
    value: Any
    unit: str
    metric_type: MetricType
    timestamp: datetime
    tags: Dict[str, str] = None

@dataclass
class Alert:
    """Represents a system alert."""
    id: str
    level: AlertLevel
    title: str
    message: str
    metric_name: Optional[str] = None
    threshold: Optional[float] = None
    current_value: Optional[float] = None
    timestamp: datetime = None
    acknowledged: bool = False
    resolved: bool = False
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class RealTimeMonitor:
    """Real-time monitoring system for the Movember AI Rules System."""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or self._get_default_config()
        self.metrics_history = []
        self.active_alerts = []
        self.alert_handlers = []
        self.monitoring_tasks = []
        self.is_running = False
        self.db_path = Path("monitoring/metrics.db")
        self.db_path.parent.mkdir(exist_ok=True)
        
        # Initialize database
        self._init_database()
        
        # Register default alert handlers
        self._register_default_handlers()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default monitoring configuration."""
        return {
            'monitoring_interval': 30,  # seconds
            'metrics_retention_days': 30,
            'alert_thresholds': {
                'api_response_time': 2.0,  # seconds
                'api_error_rate': 0.05,    # 5%
                'system_cpu_usage': 0.8,   # 80%
                'system_memory_usage': 0.85,  # 85%
                'data_freshness_hours': 24,
                'data_quality_score': 0.8,  # 80%
                'active_rules_count': 50,   # minimum rules
                'database_connections': 10,  # maximum connections
            },
            'alert_channels': {
                'console': True,
                'log_file': True,
                'email': False,
                'webhook': False
            },
            'endpoints_to_monitor': [
                '/health/',
                '/metrics/',
                '/impact/dashboard/',
                '/api/v1/rules/',
                '/api/v1/grants/'
            ]
        }
    
    def _init_database(self):
        """Initialize monitoring database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create metrics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    value REAL,
                    unit TEXT,
                    metric_type TEXT,
                    timestamp DATETIME,
                    tags TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create alerts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alerts (
                    id TEXT PRIMARY KEY,
                    level TEXT,
                    title TEXT,
                    message TEXT,
                    metric_name TEXT,
                    threshold REAL,
                    current_value REAL,
                    timestamp DATETIME,
                    acknowledged BOOLEAN DEFAULT FALSE,
                    resolved BOOLEAN DEFAULT FALSE,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indexes
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON metrics(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_metrics_name ON metrics(name)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_alerts_timestamp ON alerts(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_alerts_level ON alerts(level)')
            
            conn.commit()
            conn.close()
            logger.info("Monitoring database initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing monitoring database: {e}")
    
    def _register_default_handlers(self):
        """Register default alert handlers."""
        self.register_alert_handler(self._console_alert_handler)
        self.register_alert_handler(self._log_alert_handler)
    
    def register_alert_handler(self, handler: Callable[[Alert], None]):
        """Register a new alert handler."""
        self.alert_handlers.append(handler)
        logger.info(f"Registered alert handler: {handler.__name__}")
    
    async def start_monitoring(self):
        """Start the real-time monitoring system."""
        if self.is_running:
            logger.warning("Monitoring system is already running")
            return
        
        logger.info("Starting real-time monitoring system...")
        self.is_running = True
        
        # Start monitoring tasks
        self.monitoring_tasks = [
            asyncio.create_task(self._system_monitoring_loop()),
            asyncio.create_task(self._api_monitoring_loop()),
            asyncio.create_task(self._data_monitoring_loop()),
            asyncio.create_task(self._performance_monitoring_loop()),
            asyncio.create_task(self._business_monitoring_loop()),
            asyncio.create_task(self._cleanup_loop())
        ]
        
        logger.info("Real-time monitoring system started successfully")
    
    async def stop_monitoring(self):
        """Stop the real-time monitoring system."""
        if not self.is_running:
            logger.warning("Monitoring system is not running")
            return
        
        logger.info("Stopping real-time monitoring system...")
        self.is_running = False
        
        # Cancel all monitoring tasks
        for task in self.monitoring_tasks:
            task.cancel()
        
        # Wait for tasks to complete
        await asyncio.gather(*self.monitoring_tasks, return_exceptions=True)
        
        logger.info("Real-time monitoring system stopped")
    
    async def _system_monitoring_loop(self):
        """Monitor system-level metrics."""
        while self.is_running:
            try:
                # CPU usage
                cpu_percent = psutil.cpu_percent(interval=1)
                await self._record_metric(
                    Metric(
                        name="system_cpu_usage",
                        value=cpu_percent / 100.0,
                        unit="percentage",
                        metric_type=MetricType.SYSTEM,
                        timestamp=datetime.now(),
                        tags={"component": "system"}
                    )
                )
                
                # Memory usage
                memory = psutil.virtual_memory()
                await self._record_metric(
                    Metric(
                        name="system_memory_usage",
                        value=memory.percent / 100.0,
                        unit="percentage",
                        metric_type=MetricType.SYSTEM,
                        timestamp=datetime.now(),
                        tags={"component": "system"}
                    )
                )
                
                # Disk usage
                disk = psutil.disk_usage('/')
                await self._record_metric(
                    Metric(
                        name="system_disk_usage",
                        value=disk.percent / 100.0,
                        unit="percentage",
                        metric_type=MetricType.SYSTEM,
                        timestamp=datetime.now(),
                        tags={"component": "system"}
                    )
                )
                
                # Network I/O
                network = psutil.net_io_counters()
                await self._record_metric(
                    Metric(
                        name="system_network_bytes_sent",
                        value=network.bytes_sent,
                        unit="bytes",
                        metric_type=MetricType.SYSTEM,
                        timestamp=datetime.now(),
                        tags={"component": "system"}
                    )
                )
                
                await self._record_metric(
                    Metric(
                        name="system_network_bytes_recv",
                        value=network.bytes_recv,
                        unit="bytes",
                        metric_type=MetricType.SYSTEM,
                        timestamp=datetime.now(),
                        tags={"component": "system"}
                    )
                )
                
            except Exception as e:
                logger.error(f"Error in system monitoring: {e}")
            
            await asyncio.sleep(self.config['monitoring_interval'])
    
    async def _api_monitoring_loop(self):
        """Monitor API endpoints."""
        while self.is_running:
            try:
                async with aiohttp.ClientSession() as session:
                    for endpoint in self.config['endpoints_to_monitor']:
                        start_time = time.time()
                        
                        try:
                            url = f"http://localhost:8001{endpoint}"
                            async with session.get(url, timeout=10) as response:
                                response_time = time.time() - start_time
                                status_code = response.status
                                
                                # Record response time
                                await self._record_metric(
                                    Metric(
                                        name=f"api_response_time_{endpoint.replace('/', '_').strip('_')}",
                                        value=response_time,
                                        unit="seconds",
                                        metric_type=MetricType.API,
                                        timestamp=datetime.now(),
                                        tags={"endpoint": endpoint, "status_code": str(status_code)}
                                    )
                                )
                                
                                # Record status
                                is_success = 200 <= status_code < 400
                                await self._record_metric(
                                    Metric(
                                        name=f"api_status_{endpoint.replace('/', '_').strip('_')}",
                                        value=1 if is_success else 0,
                                        unit="boolean",
                                        metric_type=MetricType.API,
                                        timestamp=datetime.now(),
                                        tags={"endpoint": endpoint, "status_code": str(status_code)}
                                    )
                                )
                                
                        except Exception as e:
                            response_time = time.time() - start_time
                            await self._record_metric(
                                Metric(
                                    name=f"api_response_time_{endpoint.replace('/', '_').strip('_')}",
                                    value=response_time,
                                    unit="seconds",
                                    metric_type=MetricType.API,
                                    timestamp=datetime.now(),
                                    tags={"endpoint": endpoint, "error": str(e)}
                                )
                            )
                            
                            await self._record_metric(
                                Metric(
                                    name=f"api_status_{endpoint.replace('/', '_').strip('_')}",
                                    value=0,
                                    unit="boolean",
                                    metric_type=MetricType.API,
                                    timestamp=datetime.now(),
                                    tags={"endpoint": endpoint, "error": str(e)}
                                )
                            )
                
            except Exception as e:
                logger.error(f"Error in API monitoring: {e}")
            
            await asyncio.sleep(self.config['monitoring_interval'])
    
    async def _data_monitoring_loop(self):
        """Monitor data quality and freshness."""
        while self.is_running:
            try:
                # Check data freshness
                await self._check_data_freshness()
                
                # Check data quality
                await self._check_data_quality()
                
                # Check data source availability
                await self._check_data_sources()
                
            except Exception as e:
                logger.error(f"Error in data monitoring: {e}")
            
            await asyncio.sleep(self.config['monitoring_interval'] * 2)  # Less frequent
    
    async def _performance_monitoring_loop(self):
        """Monitor application performance metrics."""
        while self.is_running:
            try:
                # Check active rules count
                await self._check_active_rules()
                
                # Check database connections
                await self._check_database_connections()
                
                # Check application uptime
                await self._check_application_uptime()
                
            except Exception as e:
                logger.error(f"Error in performance monitoring: {e}")
            
            await asyncio.sleep(self.config['monitoring_interval'])
    
    async def _business_monitoring_loop(self):
        """Monitor business metrics."""
        while self.is_running:
            try:
                # Check impact metrics
                await self._check_impact_metrics()
                
                # Check grant success rates
                await self._check_grant_metrics()
                
                # Check user engagement
                await self._check_user_engagement()
                
            except Exception as e:
                logger.error(f"Error in business monitoring: {e}")
            
            await asyncio.sleep(self.config['monitoring_interval'] * 3)  # Less frequent
    
    async def _cleanup_loop(self):
        """Clean up old metrics and alerts."""
        while self.is_running:
            try:
                await self._cleanup_old_metrics()
                await self._cleanup_resolved_alerts()
                
            except Exception as e:
                logger.error(f"Error in cleanup: {e}")
            
            await asyncio.sleep(3600)  # Run cleanup every hour
    
    async def _check_data_freshness(self):
        """Check if data is fresh."""
        try:
            # Check when last data update occurred
            last_update = await self._get_last_data_update()
            if last_update:
                hours_since_update = (datetime.now() - last_update).total_seconds() / 3600
                
                await self._record_metric(
                    Metric(
                        name="data_freshness_hours",
                        value=hours_since_update,
                        unit="hours",
                        metric_type=MetricType.DATA,
                        timestamp=datetime.now(),
                        tags={"component": "data"}
                    )
                )
                
                # Check threshold
                threshold = self.config['alert_thresholds']['data_freshness_hours']
                if hours_since_update > threshold:
                    await self._create_alert(
                        AlertLevel.WARNING,
                        "Data Freshness Alert",
                        f"Data is {hours_since_update:.1f} hours old (threshold: {threshold} hours)",
                        "data_freshness_hours",
                        threshold,
                        hours_since_update
                    )
        
        except Exception as e:
            logger.error(f"Error checking data freshness: {e}")
    
    async def _check_data_quality(self):
        """Check data quality metrics."""
        try:
            # Simulate data quality check
            quality_score = 0.85  # This would be calculated from actual data
            
            await self._record_metric(
                Metric(
                    name="data_quality_score",
                    value=quality_score,
                    unit="percentage",
                    metric_type=MetricType.DATA,
                    timestamp=datetime.now(),
                    tags={"component": "data"}
                )
            )
            
            # Check threshold
            threshold = self.config['alert_thresholds']['data_quality_score']
            if quality_score < threshold:
                await self._create_alert(
                    AlertLevel.WARNING,
                    "Data Quality Alert",
                    f"Data quality score is {quality_score:.2f} (threshold: {threshold})",
                    "data_quality_score",
                    threshold,
                    quality_score
                )
        
        except Exception as e:
            logger.error(f"Error checking data quality: {e}")
    
    async def _check_data_sources(self):
        """Check data source availability."""
        try:
            # Check if data sources are responding
            sources = ['aihw', 'pubmed', 'nhmrc', 'government_api']
            available_sources = 0
            
            for source in sources:
                # Simulate source availability check
                is_available = True  # This would be an actual check
                if is_available:
                    available_sources += 1
            
            availability_rate = available_sources / len(sources)
            
            await self._record_metric(
                Metric(
                    name="data_source_availability",
                    value=availability_rate,
                    unit="percentage",
                    metric_type=MetricType.DATA,
                    timestamp=datetime.now(),
                    tags={"component": "data"}
                )
            )
            
            if availability_rate < 0.8:
                await self._create_alert(
                    AlertLevel.WARNING,
                    "Data Source Alert",
                    f"Only {availability_rate:.1%} of data sources are available",
                    "data_source_availability",
                    0.8,
                    availability_rate
                )
        
        except Exception as e:
            logger.error(f"Error checking data sources: {e}")
    
    async def _check_active_rules(self):
        """Check number of active rules."""
        try:
            # Simulate active rules count
            active_rules = 75  # This would be an actual count
            
            await self._record_metric(
                Metric(
                    name="active_rules_count",
                    value=active_rules,
                    unit="count",
                    metric_type=MetricType.PERFORMANCE,
                    timestamp=datetime.now(),
                    tags={"component": "rules_engine"}
                )
            )
            
            # Check threshold
            threshold = self.config['alert_thresholds']['active_rules_count']
            if active_rules < threshold:
                await self._create_alert(
                    AlertLevel.WARNING,
                    "Active Rules Alert",
                    f"Only {active_rules} rules are active (threshold: {threshold})",
                    "active_rules_count",
                    threshold,
                    active_rules
                )
        
        except Exception as e:
            logger.error(f"Error checking active rules: {e}")
    
    async def _check_database_connections(self):
        """Check database connection count."""
        try:
            # Simulate database connection count
            connections = 5  # This would be an actual count
            
            await self._record_metric(
                Metric(
                    name="database_connections",
                    value=connections,
                    unit="count",
                    metric_type=MetricType.PERFORMANCE,
                    timestamp=datetime.now(),
                    tags={"component": "database"}
                )
            )
            
            # Check threshold
            threshold = self.config['alert_thresholds']['database_connections']
            if connections > threshold:
                await self._create_alert(
                    AlertLevel.WARNING,
                    "Database Connections Alert",
                    f"{connections} database connections (threshold: {threshold})",
                    "database_connections",
                    threshold,
                    connections
                )
        
        except Exception as e:
            logger.error(f"Error checking database connections: {e}")
    
    async def _check_application_uptime(self):
        """Check application uptime."""
        try:
            # Simulate uptime calculation
            uptime_hours = 168  # 1 week
            
            await self._record_metric(
                Metric(
                    name="application_uptime",
                    value=uptime_hours,
                    unit="hours",
                    metric_type=MetricType.PERFORMANCE,
                    timestamp=datetime.now(),
                    tags={"component": "application"}
                )
            )
        
        except Exception as e:
            logger.error(f"Error checking application uptime: {e}")
    
    async def _check_impact_metrics(self):
        """Check business impact metrics."""
        try:
            # Simulate impact metrics
            people_reached = 8500000
            funding_raised = 125000000
            
            await self._record_metric(
                Metric(
                    name="people_reached",
                    value=people_reached,
                    unit="people",
                    metric_type=MetricType.BUSINESS,
                    timestamp=datetime.now(),
                    tags={"component": "impact"}
                )
            )
            
            await self._record_metric(
                Metric(
                    name="funding_raised",
                    value=funding_raised,
                    unit="AUD",
                    metric_type=MetricType.BUSINESS,
                    timestamp=datetime.now(),
                    tags={"component": "impact"}
                )
            )
        
        except Exception as e:
            logger.error(f"Error checking impact metrics: {e}")
    
    async def _check_grant_metrics(self):
        """Check grant-related metrics."""
        try:
            # Simulate grant metrics
            grant_success_rate = 0.75
            total_grants = 450
            
            await self._record_metric(
                Metric(
                    name="grant_success_rate",
                    value=grant_success_rate,
                    unit="percentage",
                    metric_type=MetricType.BUSINESS,
                    timestamp=datetime.now(),
                    tags={"component": "grants"}
                )
            )
            
            await self._record_metric(
                Metric(
                    name="total_grants",
                    value=total_grants,
                    unit="count",
                    metric_type=MetricType.BUSINESS,
                    timestamp=datetime.now(),
                    tags={"component": "grants"}
                )
            )
        
        except Exception as e:
            logger.error(f"Error checking grant metrics: {e}")
    
    async def _check_user_engagement(self):
        """Check user engagement metrics."""
        try:
            # Simulate user engagement metrics
            daily_active_users = 1250
            session_duration = 8.5  # minutes
            
            await self._record_metric(
                Metric(
                    name="daily_active_users",
                    value=daily_active_users,
                    unit="users",
                    metric_type=MetricType.BUSINESS,
                    timestamp=datetime.now(),
                    tags={"component": "engagement"}
                )
            )
            
            await self._record_metric(
                Metric(
                    name="session_duration",
                    value=session_duration,
                    unit="minutes",
                    metric_type=MetricType.BUSINESS,
                    timestamp=datetime.now(),
                    tags={"component": "engagement"}
                )
            )
        
        except Exception as e:
            logger.error(f"Error checking user engagement: {e}")
    
    async def _record_metric(self, metric: Metric):
        """Record a metric to the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO metrics (name, value, unit, metric_type, timestamp, tags)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                metric.name,
                metric.value,
                metric.unit,
                metric.metric_type.value,
                metric.timestamp.isoformat(),
                json.dumps(metric.tags) if metric.tags else None
            ))
            
            conn.commit()
            conn.close()
            
            # Check for alerts
            await self._check_metric_alerts(metric)
            
        except Exception as e:
            logger.error(f"Error recording metric: {e}")
    
    async def _check_metric_alerts(self, metric: Metric):
        """Check if a metric should trigger an alert."""
        try:
            thresholds = self.config['alert_thresholds']
            
            if metric.name in thresholds:
                threshold = thresholds[metric.name]
                current_value = float(metric.value)
                
                # Check if threshold is exceeded
                if metric.name in ['api_response_time', 'system_cpu_usage', 'system_memory_usage', 'data_freshness_hours']:
                    if current_value > threshold:
                        await self._create_alert(
                            AlertLevel.WARNING,
                            f"{metric.name.replace('_', ' ').title()} Alert",
                            f"{metric.name} is {current_value:.2f} (threshold: {threshold})",
                            metric.name,
                            threshold,
                            current_value
                        )
                
                elif metric.name in ['data_quality_score', 'active_rules_count']:
                    if current_value < threshold:
                        await self._create_alert(
                            AlertLevel.WARNING,
                            f"{metric.name.replace('_', ' ').title()} Alert",
                            f"{metric.name} is {current_value:.2f} (threshold: {threshold})",
                            metric.name,
                            threshold,
                            current_value
                        )
        
        except Exception as e:
            logger.error(f"Error checking metric alerts: {e}")
    
    async def _create_alert(self, level: AlertLevel, title: str, message: str, 
                          metric_name: str = None, threshold: float = None, 
                          current_value: float = None):
        """Create and store an alert."""
        try:
            alert_id = f"{metric_name}_{int(time.time())}" if metric_name else f"alert_{int(time.time())}"
            
            alert = Alert(
                id=alert_id,
                level=level,
                title=title,
                message=message,
                metric_name=metric_name,
                threshold=threshold,
                current_value=current_value
            )
            
            # Store alert in database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO alerts 
                (id, level, title, message, metric_name, threshold, current_value, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                alert.id,
                alert.level.value,
                alert.title,
                alert.message,
                alert.metric_name,
                alert.threshold,
                alert.current_value,
                alert.timestamp.isoformat()
            ))
            
            conn.commit()
            conn.close()
            
            # Add to active alerts
            self.active_alerts.append(alert)
            
            # Trigger alert handlers
            for handler in self.alert_handlers:
                try:
                    handler(alert)
                except Exception as e:
                    logger.error(f"Error in alert handler {handler.__name__}: {e}")
            
            logger.info(f"Alert created: {alert.title} ({alert.level.value})")
        
        except Exception as e:
            logger.error(f"Error creating alert: {e}")
    
    def _console_alert_handler(self, alert: Alert):
        """Console alert handler."""
        if self.config['alert_channels']['console']:
            print(f"[{alert.level.value.upper()}] {alert.title}: {alert.message}")
    
    def _log_alert_handler(self, alert: Alert):
        """Log file alert handler."""
        if self.config['alert_channels']['log_file']:
            log_level = getattr(logging, alert.level.value.upper())
            logger.log(log_level, f"ALERT: {alert.title} - {alert.message}")
    
    async def _get_last_data_update(self) -> Optional[datetime]:
        """Get the timestamp of the last data update."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT timestamp FROM metrics 
                WHERE name LIKE '%data%' 
                ORDER BY timestamp DESC 
                LIMIT 1
            ''')
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return datetime.fromisoformat(result[0])
            return None
        
        except Exception as e:
            logger.error(f"Error getting last data update: {e}")
            return None
    
    async def _cleanup_old_metrics(self):
        """Clean up old metrics from the database."""
        try:
            retention_days = self.config['metrics_retention_days']
            cutoff_date = datetime.now() - timedelta(days=retention_days)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM metrics WHERE timestamp < ?', (cutoff_date.isoformat(),))
            deleted_count = cursor.rowcount
            
            conn.commit()
            conn.close()
            
            if deleted_count > 0:
                logger.info(f"Cleaned up {deleted_count} old metrics")
        
        except Exception as e:
            logger.error(f"Error cleaning up old metrics: {e}")
    
    async def _cleanup_resolved_alerts(self):
        """Clean up resolved alerts."""
        try:
            # Remove resolved alerts older than 7 days
            cutoff_date = datetime.now() - timedelta(days=7)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM alerts WHERE resolved = TRUE AND timestamp < ?', (cutoff_date.isoformat(),))
            deleted_count = cursor.rowcount
            
            conn.commit()
            conn.close()
            
            if deleted_count > 0:
                logger.info(f"Cleaned up {deleted_count} resolved alerts")
        
        except Exception as e:
            logger.error(f"Error cleaning up resolved alerts: {e}")
    
    async def get_monitoring_summary(self) -> Dict[str, Any]:
        """Get a summary of current monitoring status."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get recent metrics count
            cursor.execute('SELECT COUNT(*) FROM metrics WHERE timestamp > datetime("now", "-1 hour")')
            recent_metrics = cursor.fetchone()[0]
            
            # Get active alerts count
            cursor.execute('SELECT COUNT(*) FROM alerts WHERE resolved = FALSE')
            active_alerts = cursor.fetchone()[0]
            
            # Get alert counts by level
            cursor.execute('SELECT level, COUNT(*) FROM alerts WHERE resolved = FALSE GROUP BY level')
            alerts_by_level = dict(cursor.fetchall())
            
            conn.close()
            
            return {
                'timestamp': datetime.now().isoformat(),
                'is_running': self.is_running,
                'recent_metrics_count': recent_metrics,
                'active_alerts_count': active_alerts,
                'alerts_by_level': alerts_by_level,
                'monitoring_interval': self.config['monitoring_interval'],
                'endpoints_monitored': len(self.config['endpoints_to_monitor'])
            }
        
        except Exception as e:
            logger.error(f"Error getting monitoring summary: {e}")
            return {'error': str(e)}

# Convenience function for easy integration
async def get_real_time_monitor(config: Dict[str, Any] = None) -> RealTimeMonitor:
    """Get initialized real-time monitor."""
    monitor = RealTimeMonitor(config)
    await monitor.start_monitoring()
    return monitor

if __name__ == "__main__":
    # Test the real-time monitoring system
    async def test():
        print("Testing Real-time Monitoring System...")
        
        # Create monitor with custom config
        config = {
            'monitoring_interval': 10,  # Faster for testing
            'alert_thresholds': {
                'api_response_time': 1.0,
                'system_cpu_usage': 0.5,
                'data_freshness_hours': 1
            }
        }
        
        monitor = RealTimeMonitor(config)
        
        # Start monitoring
        await monitor.start_monitoring()
        
        # Let it run for a bit
        await asyncio.sleep(30)
        
        # Get summary
        summary = await monitor.get_monitoring_summary()
        print(f"Monitoring Summary: {summary}")
        
        # Stop monitoring
        await monitor.stop_monitoring()
        
        print("Real-time Monitoring System test completed!")
    
    asyncio.run(test())
