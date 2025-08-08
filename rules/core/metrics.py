"""
Metrics Collector

Tracks performance metrics and execution statistics for the rule engine.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import time
import threading
import logging
from datetime import datetime, timedelta
from collections import defaultdict, deque
import statistics

logger = logging.getLogger(__name__)


@dataclass
class RuleMetrics:
    """Metrics for a specific rule."""
    rule_name: str
    total_executions: int = 0
    successful_executions: int = 0
    failed_executions: int = 0
    total_execution_time: float = 0.0
    min_execution_time: float = float('inf')
    max_execution_time: float = 0.0
    recent_execution_times: deque = field(default_factory=lambda: deque(maxlen=100))
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_executions == 0:
            return 0.0
        return self.successful_executions / self.total_executions
    
    @property
    def average_execution_time(self) -> float:
        """Calculate average execution time."""
        if self.total_executions == 0:
            return 0.0
        return self.total_execution_time / self.total_executions
    
    @property
    def median_execution_time(self) -> float:
        """Calculate median execution time."""
        if not self.recent_execution_times:
            return 0.0
        return statistics.median(self.recent_execution_times)
    
    def record_execution(self, execution_time: float, success: bool) -> None:
        """Record an execution."""
        self.total_executions += 1
        self.total_execution_time += execution_time
        self.recent_execution_times.append(execution_time)
        
        if success:
            self.successful_executions += 1
        else:
            self.failed_executions += 1
        
        # Update min/max
        if execution_time < self.min_execution_time:
            self.min_execution_time = execution_time
        if execution_time > self.max_execution_time:
            self.max_execution_time = execution_time
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'rule_name': self.rule_name,
            'total_executions': self.total_executions,
            'successful_executions': self.successful_executions,
            'failed_executions': self.failed_executions,
            'success_rate': self.success_rate,
            'total_execution_time': self.total_execution_time,
            'average_execution_time': self.average_execution_time,
            'median_execution_time': self.median_execution_time,
            'min_execution_time': self.min_execution_time if self.min_execution_time != float('inf') else 0.0,
            'max_execution_time': self.max_execution_time
        }


@dataclass
class SystemMetrics:
    """System-wide metrics."""
    total_rules_executed: int = 0
    total_batch_executions: int = 0
    total_execution_time: float = 0.0
    peak_concurrent_rules: int = 0
    current_concurrent_rules: int = 0
    uptime_start: datetime = field(default_factory=datetime.now)
    recent_batch_times: deque = field(default_factory=lambda: deque(maxlen=100))
    
    @property
    def uptime(self) -> timedelta:
        """Calculate uptime."""
        return datetime.now() - self.uptime_start
    
    @property
    def average_batch_time(self) -> float:
        """Calculate average batch execution time."""
        if not self.recent_batch_times:
            return 0.0
        return statistics.mean(self.recent_batch_times)
    
    def record_batch_execution(self, rule_count: int, execution_time: float) -> None:
        """Record a batch execution."""
        self.total_batch_executions += 1
        self.total_rules_executed += rule_count
        self.total_execution_time += execution_time
        self.recent_batch_times.append(execution_time)
        
        # Update concurrent rules tracking
        self.current_concurrent_rules = rule_count
        if rule_count > self.peak_concurrent_rules:
            self.peak_concurrent_rules = rule_count
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'total_rules_executed': self.total_rules_executed,
            'total_batch_executions': self.total_batch_executions,
            'total_execution_time': self.total_execution_time,
            'average_batch_time': self.average_batch_time,
            'peak_concurrent_rules': self.peak_concurrent_rules,
            'current_concurrent_rules': self.current_concurrent_rules,
            'uptime_seconds': self.uptime.total_seconds()
        }


class MetricsCollector:
    """Collects and manages metrics for the rule engine."""
    
    def __init__(self):
        self._lock = threading.Lock()
        self.system_metrics = SystemMetrics()
        self.rule_metrics: Dict[str, RuleMetrics] = defaultdict(lambda: RuleMetrics(""))
        
        # Performance tracking
        self.performance_thresholds = {
            'slow_execution_threshold': 5.0,  # seconds
            'error_rate_threshold': 0.1,  # 10%
            'memory_usage_threshold': 0.8  # 80%
        }
        
        # Alerts
        self.alerts: List[Dict[str, Any]] = []
    
    def record_rule_execution(self, rule_name: str, execution_time: float, success: bool) -> None:
        """Record a rule execution."""
        with self._lock:
            if rule_name not in self.rule_metrics:
                self.rule_metrics[rule_name] = RuleMetrics(rule_name)
            
            self.rule_metrics[rule_name].record_execution(execution_time, success)
            
            # Check for performance issues
            self._check_performance_alerts(rule_name, execution_time, success)
    
    def record_batch_execution(self, rule_count: int, execution_time: float) -> None:
        """Record a batch execution."""
        with self._lock:
            self.system_metrics.record_batch_execution(rule_count, execution_time)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all metrics."""
        with self._lock:
            return {
                'system': self.system_metrics.to_dict(),
                'rules': {
                    name: metrics.to_dict() 
                    for name, metrics in self.rule_metrics.items()
                },
                'alerts': self.alerts[-10:],  # Last 10 alerts
                'performance_thresholds': self.performance_thresholds
            }
    
    def get_rule_metrics(self, rule_name: str) -> Optional[Dict[str, Any]]:
        """Get metrics for a specific rule."""
        with self._lock:
            if rule_name in self.rule_metrics:
                return self.rule_metrics[rule_name].to_dict()
            return None
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get system metrics."""
        with self._lock:
            return self.system_metrics.to_dict()
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get a performance summary."""
        with self._lock:
            if not self.rule_metrics:
                return {'message': 'No rules executed yet'}
            
            # Calculate overall statistics
            total_rules = len(self.rule_metrics)
            total_executions = sum(m.total_executions for m in self.rule_metrics.values())
            total_successful = sum(m.successful_executions for m in self.rule_metrics.values())
            total_failed = sum(m.failed_executions for m in self.rule_metrics.values())
            
            overall_success_rate = total_successful / total_executions if total_executions > 0 else 0.0
            
            # Find slowest and most error-prone rules
            slowest_rule = max(self.rule_metrics.values(), key=lambda m: m.average_execution_time)
            most_error_prone = min(self.rule_metrics.values(), key=lambda m: m.success_rate)
            
            return {
                'total_rules': total_rules,
                'total_executions': total_executions,
                'overall_success_rate': overall_success_rate,
                'slowest_rule': {
                    'name': slowest_rule.rule_name,
                    'average_time': slowest_rule.average_execution_time
                },
                'most_error_prone_rule': {
                    'name': most_error_prone.rule_name,
                    'success_rate': most_error_prone.success_rate
                },
                'system_uptime_seconds': self.system_metrics.uptime.total_seconds()
            }
    
    def set_performance_thresholds(self, thresholds: Dict[str, float]) -> None:
        """Set performance thresholds."""
        with self._lock:
            self.performance_thresholds.update(thresholds)
    
    def get_alerts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent alerts."""
        with self._lock:
            return self.alerts[-limit:]
    
    def clear_alerts(self) -> None:
        """Clear all alerts."""
        with self._lock:
            self.alerts.clear()
    
    def reset(self) -> None:
        """Reset all metrics."""
        with self._lock:
            self.system_metrics = SystemMetrics()
            self.rule_metrics.clear()
            self.alerts.clear()
    
    def _check_performance_alerts(self, rule_name: str, execution_time: float, success: bool) -> None:
        """Check for performance issues and create alerts."""
        rule_metrics = self.rule_metrics[rule_name]
        
        # Check for slow execution
        if execution_time > self.performance_thresholds['slow_execution_threshold']:
            self._add_alert(
                'slow_execution',
                f"Rule '{rule_name}' took {execution_time:.2f}s to execute",
                {'rule_name': rule_name, 'execution_time': execution_time}
            )
        
        # Check for high error rate
        if rule_metrics.total_executions >= 10:  # Only check after some executions
            error_rate = 1 - rule_metrics.success_rate
            if error_rate > self.performance_thresholds['error_rate_threshold']:
                self._add_alert(
                    'high_error_rate',
                    f"Rule '{rule_name}' has {error_rate:.1%} error rate",
                    {'rule_name': rule_name, 'error_rate': error_rate}
                )
        
        # Check for consecutive failures
        if not success and rule_metrics.failed_executions >= 3:
            self._add_alert(
                'consecutive_failures',
                f"Rule '{rule_name}' has {rule_metrics.failed_executions} consecutive failures",
                {'rule_name': rule_name, 'failure_count': rule_metrics.failed_executions}
            )
    
    def _add_alert(self, alert_type: str, message: str, details: Dict[str, Any]) -> None:
        """Add an alert."""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'type': alert_type,
            'message': message,
            'details': details
        }
        
        self.alerts.append(alert)
        
        # Keep only last 100 alerts
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-100:]
        
        logger.warning(f"PERFORMANCE ALERT: {message}")
    
    def export_metrics(self, format: str = 'json') -> str:
        """Export metrics in the specified format."""
        metrics = self.get_metrics()
        
        if format.lower() == 'json':
            import json
            return json.dumps(metrics, indent=2, default=str)
        elif format.lower() == 'csv':
            return self._export_csv(metrics)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _export_csv(self, metrics: Dict[str, Any]) -> str:
        """Export metrics as CSV."""
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write system metrics
        writer.writerow(['Metric', 'Value'])
        for key, value in metrics['system'].items():
            writer.writerow([f"system_{key}", value])
        
        # Write rule metrics
        writer.writerow([])
        writer.writerow(['Rule', 'Total Executions', 'Success Rate', 'Avg Time'])
        for rule_name, rule_data in metrics['rules'].items():
            writer.writerow([
                rule_name,
                rule_data['total_executions'],
                f"{rule_data['success_rate']:.2%}",
                f"{rule_data['average_execution_time']:.3f}"
            ])
        
        return output.getvalue() 