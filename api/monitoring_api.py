#!/usr/bin/env python3
"""
Monitoring API for Movember AI Rules System
Provides real-time monitoring endpoints and metrics.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging

from monitoring.production_monitor import (
    ProductionMonitor, MetricType, AlertLevel, 
    production_monitor
)

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/monitoring", tags=["Monitoring"])

@router.get("/health")
async def get_monitoring_health():
    """Get monitoring system health status."""
    try:
        system_health = production_monitor.get_system_health()
        return {
            "status": "healthy",
            "timestamp": system_health.timestamp.isoformat(),
            "system_metrics": {
                "cpu_usage": f"{system_health.cpu_usage:.1f}%",
                "memory_usage": f"{system_health.memory_usage:.1f}%",
                "disk_usage": f"{system_health.disk_usage:.1f}%",
                "uptime_hours": f"{system_health.uptime / 3600:.1f}",
                "active_connections": system_health.active_connections
            },
            "monitoring_active": production_monitor.monitoring_active
        }
    except Exception as e:
        logger.error(f"Error getting monitoring health: {e}")
        raise HTTPException(status_code=500, detail="Error getting monitoring health")

@router.get("/metrics")
async def get_metrics(
    metric_type: Optional[str] = None,
    limit: int = 100,
    hours: int = 24
):
    """Get recent metrics."""
    try:
        # Convert metric_type string to enum
        metric_type_enum = None
        if metric_type:
            try:
                metric_type_enum = MetricType(metric_type)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid metric type: {metric_type}")
        
        metrics = production_monitor.get_recent_metrics(metric_type_enum, limit)
        
        # Filter by time if specified
        if hours > 0:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            metrics = [m for m in metrics if m.timestamp > cutoff_time]
        
        return {
            "status": "success",
            "total_metrics": len(metrics),
            "metric_type": metric_type,
            "hours": hours,
            "metrics": [
                {
                    "metric_id": metric.metric_id,
                    "name": metric.name,
                    "value": metric.value,
                    "unit": metric.unit,
                    "metric_type": metric.metric_type.value,
                    "timestamp": metric.timestamp.isoformat(),
                    "tags": metric.tags
                }
                for metric in metrics
            ]
        }
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        raise HTTPException(status_code=500, detail="Error getting metrics")

@router.get("/alerts")
async def get_alerts(active_only: bool = True):
    """Get alerts."""
    try:
        if active_only:
            alerts = production_monitor.get_active_alerts()
        else:
            # Get all alerts from database
            alerts = production_monitor.alerts
        
        return {
            "status": "success",
            "total_alerts": len(alerts),
            "active_only": active_only,
            "alerts": [
                {
                    "alert_id": alert.alert_id,
                    "level": alert.level.value,
                    "title": alert.title,
                    "message": alert.message,
                    "timestamp": alert.timestamp.isoformat(),
                    "metric_type": alert.metric_type.value,
                    "value": alert.value,
                    "threshold": alert.threshold,
                    "resolved": alert.resolved,
                    "resolved_at": alert.resolved_at.isoformat() if alert.resolved_at else None
                }
                for alert in alerts
            ]
        }
    except Exception as e:
        logger.error(f"Error getting alerts: {e}")
        raise HTTPException(status_code=500, detail="Error getting alerts")

@router.get("/dashboard")
async def get_monitoring_dashboard():
    """Get comprehensive monitoring dashboard data."""
    try:
        # Get system health
        system_health = production_monitor.get_system_health()
        
        # Get recent metrics by type
        system_metrics = production_monitor.get_recent_metrics(MetricType.SYSTEM, 10)
        application_metrics = production_monitor.get_recent_metrics(MetricType.APPLICATION, 10)
        database_metrics = production_monitor.get_recent_metrics(MetricType.DATABASE, 10)
        api_metrics = production_monitor.get_recent_metrics(MetricType.API, 10)
        
        # Get active alerts
        active_alerts = production_monitor.get_active_alerts()
        
        # Calculate summary statistics
        alert_summary = {
            "total": len(active_alerts),
            "critical": len([a for a in active_alerts if a.level == AlertLevel.CRITICAL]),
            "error": len([a for a in active_alerts if a.level == AlertLevel.ERROR]),
            "warning": len([a for a in active_alerts if a.level == AlertLevel.WARNING]),
            "info": len([a for a in active_alerts if a.level == AlertLevel.INFO])
        }
        
        # Get latest values for key metrics
        latest_metrics = {}
        for metric in system_metrics + application_metrics + database_metrics + api_metrics:
            if metric.name not in latest_metrics or metric.timestamp > latest_metrics[metric.name]["timestamp"]:
                latest_metrics[metric.name] = {
                    "value": metric.value,
                    "unit": metric.unit,
                    "timestamp": metric.timestamp
                }
        
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "monitoring_active": production_monitor.monitoring_active,
            "system_health": {
                "cpu_usage": f"{system_health.cpu_usage:.1f}%",
                "memory_usage": f"{system_health.memory_usage:.1f}%",
                "disk_usage": f"{system_health.disk_usage:.1f}%",
                "uptime_hours": f"{system_health.uptime / 3600:.1f}",
                "active_connections": system_health.active_connections
            },
            "latest_metrics": latest_metrics,
            "alert_summary": alert_summary,
            "recent_alerts": [
                {
                    "level": alert.level.value,
                    "title": alert.title,
                    "timestamp": alert.timestamp.isoformat()
                }
                for alert in active_alerts[:5]  # Show last 5 alerts
            ]
        }
    except Exception as e:
        logger.error(f"Error getting monitoring dashboard: {e}")
        raise HTTPException(status_code=500, detail="Error getting monitoring dashboard")

@router.post("/start")
async def start_monitoring(background_tasks: BackgroundTasks):
    """Start the monitoring system."""
    try:
        if not production_monitor.monitoring_active:
            background_tasks.add_task(production_monitor.start_monitoring)
            return {
                "status": "success",
                "message": "Monitoring system started",
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "status": "info",
                "message": "Monitoring system already running",
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        logger.error(f"Error starting monitoring: {e}")
        raise HTTPException(status_code=500, detail="Error starting monitoring")

@router.post("/stop")
async def stop_monitoring():
    """Stop the monitoring system."""
    try:
        production_monitor.stop_monitoring()
        return {
            "status": "success",
            "message": "Monitoring system stopped",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error stopping monitoring: {e}")
        raise HTTPException(status_code=500, detail="Error stopping monitoring")

@router.get("/thresholds")
async def get_thresholds():
    """Get current monitoring thresholds."""
    try:
        return {
            "status": "success",
            "thresholds": production_monitor.thresholds,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting thresholds: {e}")
        raise HTTPException(status_code=500, detail="Error getting thresholds")

@router.put("/thresholds")
async def update_thresholds(thresholds: Dict[str, float]):
    """Update monitoring thresholds."""
    try:
        # Validate thresholds
        valid_thresholds = {
            "cpu_usage", "memory_usage", "disk_usage", 
            "response_time", "error_rate", "uptime"
        }
        
        for key, value in thresholds.items():
            if key not in valid_thresholds:
                raise HTTPException(status_code=400, detail=f"Invalid threshold: {key}")
            if not isinstance(value, (int, float)) or value < 0:
                raise HTTPException(status_code=400, detail=f"Invalid value for {key}: {value}")
        
        # Update thresholds
        production_monitor.thresholds.update(thresholds)
        
        return {
            "status": "success",
            "message": "Thresholds updated",
            "thresholds": production_monitor.thresholds,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error updating thresholds: {e}")
        raise HTTPException(status_code=500, detail="Error updating thresholds")

@router.get("/performance")
async def get_performance_summary(hours: int = 24):
    """Get performance summary for the specified time period."""
    try:
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        # Get metrics for the time period
        all_metrics = production_monitor.get_recent_metrics(limit=1000)
        recent_metrics = [m for m in all_metrics if m.timestamp > cutoff_time]
        
        # Group metrics by type
        metrics_by_type = {}
        for metric in recent_metrics:
            if metric.metric_type.value not in metrics_by_type:
                metrics_by_type[metric.metric_type.value] = []
            metrics_by_type[metric.metric_type.value].append(metric)
        
        # Calculate performance statistics
        performance_summary = {}
        for metric_type, metrics in metrics_by_type.items():
            if not metrics:
                continue
                
            # Group by metric name
            metrics_by_name = {}
            for metric in metrics:
                if metric.name not in metrics_by_name:
                    metrics_by_name[metric.name] = []
                metrics_by_name[metric.name].append(metric)
            
            performance_summary[metric_type] = {}
            for name, metric_list in metrics_by_name.items():
                values = [m.value for m in metric_list]
                performance_summary[metric_type][name] = {
                    "count": len(values),
                    "min": min(values),
                    "max": max(values),
                    "avg": sum(values) / len(values),
                    "unit": metric_list[0].unit,
                    "latest": values[-1] if values else 0
                }
        
        return {
            "status": "success",
            "period_hours": hours,
            "total_metrics": len(recent_metrics),
            "performance_summary": performance_summary,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting performance summary: {e}")
        raise HTTPException(status_code=500, detail="Error getting performance summary")

# Include monitoring routes in main API
def include_monitoring_routes(app):
    """Include monitoring routes in the main FastAPI app."""
    app.include_router(router)
    logger.info("Monitoring API routes included")
