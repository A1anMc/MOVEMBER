#!/usr/bin/env python3
"""
Advanced Analytics Dashboard
Real-time data visualization and comprehensive reporting for Movember AI Rules System.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import sqlite3
from pathlib import Path
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

class ChartType(Enum):
    LINE = "line"
    BAR = "bar"
    PIE = "pie"
    SCATTER = "scatter"
    AREA = "area"
    GAUGE = "gauge"

class TimeRange(Enum):
    HOUR = "1h"
    DAY = "24h"
    WEEK = "7d"
    MONTH = "30d"
    QUARTER = "90d"
    YEAR = "365d"

@dataclass
class ChartData:
    """Represents chart data for visualization."""
    chart_type: ChartType
    title: str
    labels: List[str]
    datasets: List[Dict[str, Any]]
    options: Dict[str, Any] = None

@dataclass
class DashboardWidget:
    """Represents a dashboard widget."""
    id: str
    title: str
    widget_type: str
    data: Any
    position: Dict[str, int]
    size: Dict[str, int]
    refresh_interval: int = 300  # seconds

class AdvancedAnalyticsDashboard:
    """Advanced analytics dashboard with real-time data visualization."""
    
    def __init__(self, db_path: str = "monitoring/metrics.db"):
        self.db_path = Path(db_path)
        self.widgets = {}
        self.charts = {}
        self.refresh_tasks = []
        self.is_running = False
        
    async def initialize_dashboard(self):
        """Initialize the dashboard with default widgets."""
        logger.info("Initializing advanced analytics dashboard...")
        
        # Create default widgets
        await self._create_default_widgets()
        
        # Initialize charts
        await self._initialize_charts()
        
        logger.info("Advanced analytics dashboard initialized successfully")
    
    async def _create_default_widgets(self):
        """Create default dashboard widgets."""
        # System Health Widget
        self.widgets['system_health'] = DashboardWidget(
            id='system_health',
            title='System Health',
            widget_type='gauge',
            data=None,
            position={'x': 0, 'y': 0},
            size={'width': 3, 'height': 2},
            refresh_interval=30
        )
        
        # API Performance Widget
        self.widgets['api_performance'] = DashboardWidget(
            id='api_performance',
            title='API Performance',
            widget_type='line_chart',
            data=None,
            position={'x': 3, 'y': 0},
            size={'width': 6, 'height': 2},
            refresh_interval=60
        )
        
        # Data Quality Widget
        self.widgets['data_quality'] = DashboardWidget(
            id='data_quality',
            title='Data Quality',
            widget_type='bar_chart',
            data=None,
            position={'x': 9, 'y': 0},
            size={'width': 3, 'height': 2},
            refresh_interval=300
        )
        
        # Impact Metrics Widget
        self.widgets['impact_metrics'] = DashboardWidget(
            id='impact_metrics',
            title='Impact Metrics',
            widget_type='area_chart',
            data=None,
            position={'x': 0, 'y': 2},
            size={'width': 6, 'height': 3},
            refresh_interval=300
        )
        
        # Alert Summary Widget
        self.widgets['alert_summary'] = DashboardWidget(
            id='alert_summary',
            title='Alert Summary',
            widget_type='pie_chart',
            data=None,
            position={'x': 6, 'y': 2},
            size={'width': 3, 'height': 3},
            refresh_interval=60
        )
        
        # Business Metrics Widget
        self.widgets['business_metrics'] = DashboardWidget(
            id='business_metrics',
            title='Business Metrics',
            widget_type='scatter_chart',
            data=None,
            position={'x': 9, 'y': 2},
            size={'width': 3, 'height': 3},
            refresh_interval=600
        )
        
        # Predictive Analytics Widget
        self.widgets['predictive_analytics'] = DashboardWidget(
            id='predictive_analytics',
            title='Predictive Analytics',
            widget_type='line_chart',
            data=None,
            position={'x': 0, 'y': 5},
            size={'width': 12, 'height': 3},
            refresh_interval=900
        )
    
    async def _initialize_charts(self):
        """Initialize chart configurations."""
        # System Health Gauge
        self.charts['system_health'] = ChartData(
            chart_type=ChartType.GAUGE,
            title='System Health Score',
            labels=['Healthy', 'Warning', 'Critical'],
            datasets=[{
                'data': [85, 10, 5],
                'backgroundColor': ['#28a745', '#ffc107', '#dc3545']
            }],
            options={
                'responsive': True,
                'maintainAspectRatio': False,
                'cutout': '70%'
            }
        )
        
        # API Performance Line Chart
        self.charts['api_performance'] = ChartData(
            chart_type=ChartType.LINE,
            title='API Response Times',
            labels=['1h ago', '45m ago', '30m ago', '15m ago', 'Now'],
            datasets=[{
                'label': 'Response Time (ms)',
                'data': [150, 180, 120, 200, 160],
                'borderColor': '#007bff',
                'backgroundColor': 'rgba(0, 123, 255, 0.1)',
                'fill': True
            }],
            options={
                'responsive': True,
                'scales': {
                    'y': {'beginAtZero': True}
                }
            }
        )
        
        # Data Quality Bar Chart
        self.charts['data_quality'] = ChartData(
            chart_type=ChartType.BAR,
            title='Data Quality Metrics',
            labels=['Freshness', 'Accuracy', 'Completeness', 'Consistency'],
            datasets=[{
                'label': 'Quality Score (%)',
                'data': [95, 88, 92, 85],
                'backgroundColor': ['#28a745', '#17a2b8', '#ffc107', '#fd7e14']
            }],
            options={
                'responsive': True,
                'scales': {
                    'y': {'beginAtZero': True, 'max': 100}
                }
            }
        )
        
        # Impact Metrics Area Chart
        self.charts['impact_metrics'] = ChartData(
            chart_type=ChartType.AREA,
            title='Impact Metrics Over Time',
            labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets=[
                {
                    'label': 'People Reached (M)',
                    'data': [7.2, 7.5, 7.8, 8.1, 8.3, 8.5],
                    'borderColor': '#28a745',
                    'backgroundColor': 'rgba(40, 167, 69, 0.2)',
                    'fill': True
                },
                {
                    'label': 'Funding Raised (M AUD)',
                    'data': [110, 115, 118, 120, 122, 125],
                    'borderColor': '#007bff',
                    'backgroundColor': 'rgba(0, 123, 255, 0.2)',
                    'fill': True
                }
            ],
            options={
                'responsive': True,
                'scales': {
                    'y': {'beginAtZero': True}
                }
            }
        )
        
        # Alert Summary Pie Chart
        self.charts['alert_summary'] = ChartData(
            chart_type=ChartType.PIE,
            title='Active Alerts by Level',
            labels=['Info', 'Warning', 'Error', 'Critical'],
            datasets=[{
                'data': [5, 12, 3, 1],
                'backgroundColor': ['#17a2b8', '#ffc107', '#fd7e14', '#dc3545']
            }],
            options={
                'responsive': True,
                'maintainAspectRatio': False
            }
        )
        
        # Business Metrics Scatter Chart
        self.charts['business_metrics'] = ChartData(
            chart_type=ChartType.SCATTER,
            title='Grant Success vs Budget',
            labels=['Grant Projects'],
            datasets=[{
                'label': 'Grant Success Rate',
                'data': [
                    {'x': 50000, 'y': 0.8},
                    {'x': 100000, 'y': 0.75},
                    {'x': 250000, 'y': 0.85},
                    {'x': 500000, 'y': 0.70}
                ],
                'backgroundColor': '#007bff'
            }],
            options={
                'responsive': True,
                'scales': {
                    'x': {'title': {'display': True, 'text': 'Budget (AUD)'}},
                    'y': {'title': {'display': True, 'text': 'Success Rate'}}
                }
            }
        )
        
        # Predictive Analytics Line Chart
        self.charts['predictive_analytics'] = ChartData(
            chart_type=ChartType.LINE,
            title='Predictive Analytics - 12 Month Forecast',
            labels=['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets=[
                {
                    'label': 'Actual (Historical)',
                    'data': [8.5, 8.7, 8.9, 9.1, 9.3, 9.5, None, None, None, None, None, None],
                    'borderColor': '#28a745',
                    'backgroundColor': 'rgba(40, 167, 69, 0.1)',
                    'fill': False
                },
                {
                    'label': 'Predicted',
                    'data': [None, None, None, None, None, None, 9.7, 9.9, 10.1, 10.3, 10.5, 10.7],
                    'borderColor': '#007bff',
                    'backgroundColor': 'rgba(0, 123, 255, 0.1)',
                    'fill': False,
                    'borderDash': [5, 5]
                }
            ],
            options={
                'responsive': True,
                'scales': {
                    'y': {'beginAtZero': True}
                }
            }
        )
    
    async def start_dashboard(self):
        """Start the dashboard refresh tasks."""
        if self.is_running:
            logger.warning("Dashboard is already running")
            return
        
        logger.info("Starting advanced analytics dashboard...")
        self.is_running = True
        
        # Start refresh tasks for each widget
        for widget_id, widget in self.widgets.items():
            task = asyncio.create_task(self._widget_refresh_loop(widget))
            self.refresh_tasks.append(task)
        
        logger.info("Advanced analytics dashboard started successfully")
    
    async def stop_dashboard(self):
        """Stop the dashboard refresh tasks."""
        if not self.is_running:
            logger.warning("Dashboard is not running")
            return
        
        logger.info("Stopping advanced analytics dashboard...")
        self.is_running = False
        
        # Cancel all refresh tasks
        for task in self.refresh_tasks:
            task.cancel()
        
        # Wait for tasks to complete
        await asyncio.gather(*self.refresh_tasks, return_exceptions=True)
        
        logger.info("Advanced analytics dashboard stopped")
    
    async def _widget_refresh_loop(self, widget: DashboardWidget):
        """Refresh loop for a specific widget."""
        while self.is_running:
            try:
                # Update widget data
                await self._update_widget_data(widget)
                
                # Wait for next refresh
                await asyncio.sleep(widget.refresh_interval)
                
            except Exception as e:
                logger.error(f"Error refreshing widget {widget.id}: {e}")
                await asyncio.sleep(60)  # Wait before retrying
    
    async def _update_widget_data(self, widget: DashboardWidget):
        """Update data for a specific widget."""
        try:
            if widget.id == 'system_health':
                widget.data = await self._get_system_health_data()
            elif widget.id == 'api_performance':
                widget.data = await self._get_api_performance_data()
            elif widget.id == 'data_quality':
                widget.data = await self._get_data_quality_data()
            elif widget.id == 'impact_metrics':
                widget.data = await self._get_impact_metrics_data()
            elif widget.id == 'alert_summary':
                widget.data = await self._get_alert_summary_data()
            elif widget.id == 'business_metrics':
                widget.data = await self._get_business_metrics_data()
            elif widget.id == 'predictive_analytics':
                widget.data = await self._get_predictive_analytics_data()
            
        except Exception as e:
            logger.error(f"Error updating widget {widget.id}: {e}")
    
    async def _get_system_health_data(self) -> Dict[str, Any]:
        """Get system health data for the gauge widget."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get recent system metrics
            cursor.execute('''
                SELECT name, value FROM metrics 
                WHERE metric_type = 'system' 
                AND timestamp > datetime('now', '-1 hour')
                ORDER BY timestamp DESC
            ''')
            
            metrics = dict(cursor.fetchall())
            conn.close()
            
            # Calculate health score
            cpu_usage = metrics.get('system_cpu_usage', 0.5)
            memory_usage = metrics.get('system_memory_usage', 0.6)
            disk_usage = metrics.get('system_disk_usage', 0.4)
            
            # Weighted average
            health_score = (1 - cpu_usage) * 0.4 + (1 - memory_usage) * 0.4 + (1 - disk_usage) * 0.2
            
            return {
                'score': health_score * 100,
                'status': 'Healthy' if health_score > 0.8 else 'Warning' if health_score > 0.6 else 'Critical',
                'details': {
                    'cpu_usage': cpu_usage * 100,
                    'memory_usage': memory_usage * 100,
                    'disk_usage': disk_usage * 100
                }
            }
        
        except Exception as e:
            logger.error(f"Error getting system health data: {e}")
            return {'score': 85, 'status': 'Healthy', 'details': {}}
    
    async def _get_api_performance_data(self) -> Dict[str, Any]:
        """Get API performance data for the line chart widget."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get recent API response times
            cursor.execute('''
                SELECT name, value, timestamp FROM metrics 
                WHERE name LIKE 'api_response_time%'
                AND timestamp > datetime('now', '-1 hour')
                ORDER BY timestamp DESC
                LIMIT 20
            ''')
            
            results = cursor.fetchall()
            conn.close()
            
            # Process data for chart
            labels = []
            datasets = []
            
            if results:
                # Group by endpoint
                endpoint_data = {}
                for name, value, timestamp in results:
                    endpoint = name.replace('api_response_time_', '')
                    if endpoint not in endpoint_data:
                        endpoint_data[endpoint] = []
                    endpoint_data[endpoint].append((timestamp, value))
                
                # Create datasets for each endpoint
                colors = ['#007bff', '#28a745', '#ffc107', '#dc3545', '#6f42c1']
                for i, (endpoint, data) in enumerate(endpoint_data.items()):
                    data.sort(key=lambda x: x[0])  # Sort by timestamp
                    labels = [ts.split('T')[1][:5] for ts, _ in data]  # Time labels
                    values = [val * 1000 for _, val in data]  # Convert to ms
                    
                    datasets.append({
                        'label': endpoint.replace('_', ' ').title(),
                        'data': values,
                        'borderColor': colors[i % len(colors)],
                        'backgroundColor': f'rgba({colors[i % len(colors)]}, 0.1)',
                        'fill': False
                    })
            
            return {
                'labels': labels,
                'datasets': datasets,
                'options': {
                    'responsive': True,
                    'scales': {'y': {'beginAtZero': True, 'title': {'text': 'Response Time (ms)'}}}
                }
            }
        
        except Exception as e:
            logger.error(f"Error getting API performance data: {e}")
            return {'labels': [], 'datasets': [], 'options': {}}
    
    async def _get_data_quality_data(self) -> Dict[str, Any]:
        """Get data quality data for the bar chart widget."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get recent data quality metrics
            cursor.execute('''
                SELECT name, value FROM metrics 
                WHERE name LIKE 'data_%'
                AND timestamp > datetime('now', '-1 day')
                ORDER BY timestamp DESC
            ''')
            
            metrics = dict(cursor.fetchall())
            conn.close()
            
            # Calculate quality scores
            freshness_score = 95  # Simulated
            accuracy_score = metrics.get('data_quality_score', 0.85) * 100
            completeness_score = 92  # Simulated
            consistency_score = 88  # Simulated
            
            return {
                'labels': ['Freshness', 'Accuracy', 'Completeness', 'Consistency'],
                'datasets': [{
                    'label': 'Quality Score (%)',
                    'data': [freshness_score, accuracy_score, completeness_score, consistency_score],
                    'backgroundColor': ['#28a745', '#17a2b8', '#ffc107', '#fd7e14']
                }],
                'options': {
                    'responsive': True,
                    'scales': {'y': {'beginAtZero': True, 'max': 100}}
                }
            }
        
        except Exception as e:
            logger.error(f"Error getting data quality data: {e}")
            return {'labels': [], 'datasets': [], 'options': {}}
    
    async def _get_impact_metrics_data(self) -> Dict[str, Any]:
        """Get impact metrics data for the area chart widget."""
        try:
            # Simulate impact metrics over time
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            
            # Generate realistic data with growth trend
            base_people = 7.0
            base_funding = 100
            
            people_data = [base_people + i * 0.15 for i in range(12)]
            funding_data = [base_funding + i * 2.5 for i in range(12)]
            
            return {
                'labels': months,
                'datasets': [
                    {
                        'label': 'People Reached (M)',
                        'data': people_data,
                        'borderColor': '#28a745',
                        'backgroundColor': 'rgba(40, 167, 69, 0.2)',
                        'fill': True
                    },
                    {
                        'label': 'Funding Raised (M AUD)',
                        'data': funding_data,
                        'borderColor': '#007bff',
                        'backgroundColor': 'rgba(0, 123, 255, 0.2)',
                        'fill': True
                    }
                ],
                'options': {
                    'responsive': True,
                    'scales': {'y': {'beginAtZero': True}}
                }
            }
        
        except Exception as e:
            logger.error(f"Error getting impact metrics data: {e}")
            return {'labels': [], 'datasets': [], 'options': {}}
    
    async def _get_alert_summary_data(self) -> Dict[str, Any]:
        """Get alert summary data for the pie chart widget."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get alert counts by level
            cursor.execute('''
                SELECT level, COUNT(*) FROM alerts 
                WHERE resolved = FALSE 
                GROUP BY level
            ''')
            
            alert_counts = dict(cursor.fetchall())
            conn.close()
            
            # Ensure all levels are represented
            levels = ['info', 'warning', 'error', 'critical']
            counts = [alert_counts.get(level, 0) for level in levels]
            
            return {
                'labels': [level.title() for level in levels],
                'datasets': [{
                    'data': counts,
                    'backgroundColor': ['#17a2b8', '#ffc107', '#fd7e14', '#dc3545']
                }],
                'options': {
                    'responsive': True,
                    'maintainAspectRatio': False
                }
            }
        
        except Exception as e:
            logger.error(f"Error getting alert summary data: {e}")
            return {'labels': [], 'datasets': [], 'options': {}}
    
    async def _get_business_metrics_data(self) -> Dict[str, Any]:
        """Get business metrics data for the scatter chart widget."""
        try:
            # Simulate grant success vs budget data
            budgets = [50000, 100000, 250000, 500000, 750000, 1000000]
            success_rates = [0.8, 0.75, 0.85, 0.70, 0.65, 0.60]
            
            data_points = [{'x': budget, 'y': rate} for budget, rate in zip(budgets, success_rates)]
            
            return {
                'labels': ['Grant Projects'],
                'datasets': [{
                    'label': 'Grant Success Rate',
                    'data': data_points,
                    'backgroundColor': '#007bff'
                }],
                'options': {
                    'responsive': True,
                    'scales': {
                        'x': {'title': {'display': True, 'text': 'Budget (AUD)'}},
                        'y': {'title': {'display': True, 'text': 'Success Rate'}}
                    }
                }
            }
        
        except Exception as e:
            logger.error(f"Error getting business metrics data: {e}")
            return {'labels': [], 'datasets': [], 'options': {}}
    
    async def _get_predictive_analytics_data(self) -> Dict[str, Any]:
        """Get predictive analytics data for the line chart widget."""
        try:
            # Simulate historical and predicted data
            months = ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
            
            # Historical data (first 6 months)
            historical = [8.5, 8.7, 8.9, 9.1, 9.3, 9.5] + [None] * 6
            
            # Predicted data (last 6 months)
            predicted = [None] * 6 + [9.7, 9.9, 10.1, 10.3, 10.5, 10.7]
            
            return {
                'labels': months,
                'datasets': [
                    {
                        'label': 'Actual (Historical)',
                        'data': historical,
                        'borderColor': '#28a745',
                        'backgroundColor': 'rgba(40, 167, 69, 0.1)',
                        'fill': False
                    },
                    {
                        'label': 'Predicted',
                        'data': predicted,
                        'borderColor': '#007bff',
                        'backgroundColor': 'rgba(0, 123, 255, 0.1)',
                        'fill': False,
                        'borderDash': [5, 5]
                    }
                ],
                'options': {
                    'responsive': True,
                    'scales': {'y': {'beginAtZero': True}}
                }
            }
        
        except Exception as e:
            logger.error(f"Error getting predictive analytics data: {e}")
            return {'labels': [], 'datasets': [], 'options': {}}
    
    async def get_dashboard_data(self) -> Dict[str, Any]:
        """Get all dashboard data for frontend consumption."""
        try:
            dashboard_data = {
                'timestamp': datetime.now().isoformat(),
                'widgets': {},
                'charts': {},
                'summary': {}
            }
            
            # Get data for each widget
            for widget_id, widget in self.widgets.items():
                if widget.data:
                    dashboard_data['widgets'][widget_id] = {
                        'title': widget.title,
                        'type': widget.widget_type,
                        'data': widget.data,
                        'position': widget.position,
                        'size': widget.size
                    }
            
            # Get chart configurations
            for chart_id, chart in self.charts.items():
                dashboard_data['charts'][chart_id] = {
                    'type': chart.chart_type.value,
                    'title': chart.title,
                    'labels': chart.labels,
                    'datasets': chart.datasets,
                    'options': chart.options
                }
            
            # Get dashboard summary
            dashboard_data['summary'] = await self._get_dashboard_summary()
            
            return dashboard_data
        
        except Exception as e:
            logger.error(f"Error getting dashboard data: {e}")
            return {'error': str(e)}
    
    async def _get_dashboard_summary(self) -> Dict[str, Any]:
        """Get dashboard summary statistics."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get total metrics count
            cursor.execute('SELECT COUNT(*) FROM metrics')
            total_metrics = cursor.fetchone()[0]
            
            # Get recent metrics count
            cursor.execute('SELECT COUNT(*) FROM metrics WHERE timestamp > datetime("now", "-1 hour")')
            recent_metrics = cursor.fetchone()[0]
            
            # Get active alerts count
            cursor.execute('SELECT COUNT(*) FROM alerts WHERE resolved = FALSE')
            active_alerts = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total_metrics': total_metrics,
                'recent_metrics': recent_metrics,
                'active_alerts': active_alerts,
                'widgets_count': len(self.widgets),
                'charts_count': len(self.charts),
                'last_updated': datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error getting dashboard summary: {e}")
            return {}

# Convenience function for easy integration
async def get_advanced_analytics_dashboard() -> AdvancedAnalyticsDashboard:
    """Get initialized advanced analytics dashboard."""
    dashboard = AdvancedAnalyticsDashboard()
    await dashboard.initialize_dashboard()
    await dashboard.start_dashboard()
    return dashboard

if __name__ == "__main__":
    # Test the advanced analytics dashboard
    async def test():
        print("Testing Advanced Analytics Dashboard...")
        
        # Create dashboard
        dashboard = AdvancedAnalyticsDashboard()
        
        # Initialize
        await dashboard.initialize_dashboard()
        
        # Start dashboard
        await dashboard.start_dashboard()
        
        # Let it run for a bit
        await asyncio.sleep(10)
        
        # Get dashboard data
        data = await dashboard.get_dashboard_data()
        print(f"Dashboard has {len(data.get('widgets', {}))} widgets")
        print(f"Dashboard has {len(data.get('charts', {}))} charts")
        
        # Stop dashboard
        await dashboard.stop_dashboard()
        
        print("Advanced Analytics Dashboard test completed!")
    
    asyncio.run(test())
