#!/usr/bin/env python3
"""
Deployment Monitoring System
High-level monitoring for real vs test data implementation.
"""

import asyncio
import logging
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

import requests
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/deployment_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

console = Console()


@dataclass
class HealthCheck:
    """Health check result."""
    name: str
    status: str  # 'healthy', 'warning', 'critical'
    response_time: float
    details: str
    timestamp: datetime
    environment: str
    data_source: str


@dataclass
class DeploymentMetrics:
    """Deployment metrics."""
    total_checks: int
    healthy_checks: int
    warning_checks: int
    critical_checks: int
    average_response_time: float
    uptime_percentage: float
    last_check: datetime
    environment: str


class DeploymentMonitor:
    """Monitors deployment health and performance."""
    
    def __init__(self):
        self.api_url = "https://movember-api.onrender.com"
        self.frontend_url = "https://movember-frontend.onrender.com"
        self.health_checks: List[HealthCheck] = []
        self.start_time = datetime.now()
        self.console = Console()
        
    async def check_api_health(self) -> HealthCheck:
        """Check API health."""
        start_time = time.time()
        try:
            response = requests.get(f"{self.api_url}/health", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                status = "healthy"
                details = f"API responding normally (HTTP {response.status_code})"
            else:
                status = "warning"
                details = f"API responding but with status {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            response_time = time.time() - start_time
            status = "critical"
            details = f"API connection failed: {str(e)}"
        
        return HealthCheck(
            name="API Health",
            status=status,
            response_time=response_time,
            details=details,
            timestamp=datetime.now(),
            environment="production",
            data_source="movember-api"
        )
    
    async def check_frontend_health(self) -> HealthCheck:
        """Check frontend health."""
        start_time = time.time()
        try:
            response = requests.get(self.frontend_url, timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                status = "healthy"
                details = f"Frontend responding normally (HTTP {response.status_code})"
            else:
                status = "warning"
                details = f"Frontend responding but with status {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            response_time = time.time() - start_time
            status = "critical"
            details = f"Frontend connection failed: {str(e)}"
        
        return HealthCheck(
            name="Frontend Health",
            status=status,
            response_time=response_time,
            details=details,
            timestamp=datetime.now(),
            environment="production",
            data_source="movember-frontend"
        )
    
    async def check_data_source_health(self) -> List[HealthCheck]:
        """Check data source health."""
        checks = []
        
        # Test data source endpoints
        data_endpoints = [
            ("/grants", "Grant Data Source"),
            ("/impact", "Impact Data Source"),
            ("/research", "Research Data Source"),
            ("/metrics", "Metrics Data Source")
        ]
        
        for endpoint, name in data_endpoints:
            start_time = time.time()
            try:
                response = requests.get(f"{self.api_url}{endpoint}", timeout=15)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    status = "healthy"
                    details = f"Data source responding (HTTP {response.status_code})"
                else:
                    status = "warning"
                    details = f"Data source responding but with status {response.status_code}"
                    
            except requests.exceptions.RequestException as e:
                response_time = time.time() - start_time
                status = "critical"
                details = f"Data source connection failed: {str(e)}"
            
            checks.append(HealthCheck(
                name=name,
                status=status,
                response_time=response_time,
                details=details,
                timestamp=datetime.now(),
                environment="production",
                data_source=endpoint
            ))
        
        return checks
    
    async def check_environment_configuration(self) -> HealthCheck:
        """Check environment configuration."""
        start_time = time.time()
        try:
            response = requests.get(f"{self.api_url}/config", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                config_data = response.json()
                use_real_data = config_data.get('use_real_data', False)
                
                if use_real_data:
                    status = "healthy"
                    details = "Production environment with real data enabled"
                else:
                    status = "warning"
                    details = "Production environment but using test data"
            else:
                status = "warning"
                details = f"Config endpoint responding but with status {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            response_time = time.time() - start_time
            status = "critical"
            details = f"Config endpoint connection failed: {str(e)}"
        
        return HealthCheck(
            name="Environment Configuration",
            status=status,
            response_time=response_time,
            details=details,
            timestamp=datetime.now(),
            environment="production",
            data_source="config"
        )
    
    async def check_data_quality(self) -> HealthCheck:
        """Check data quality metrics."""
        start_time = time.time()
        try:
            response = requests.get(f"{self.api_url}/quality", timeout=15)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                quality_data = response.json()
                overall_score = quality_data.get('overall_score', 0)
                
                if overall_score >= 0.9:
                    status = "healthy"
                    details = f"Data quality excellent ({overall_score:.2%})"
                elif overall_score >= 0.75:
                    status = "warning"
                    details = f"Data quality acceptable ({overall_score:.2%})"
                else:
                    status = "critical"
                    details = f"Data quality poor ({overall_score:.2%})"
            else:
                status = "warning"
                details = f"Quality endpoint responding but with status {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            response_time = time.time() - start_time
            status = "critical"
            details = f"Quality endpoint connection failed: {str(e)}"
        
        return HealthCheck(
            name="Data Quality",
            status=status,
            response_time=response_time,
            details=details,
            timestamp=datetime.now(),
            environment="production",
            data_source="quality"
        )
    
    async def run_health_checks(self) -> List[HealthCheck]:
        """Run all health checks."""
        logger.info("🔍 Running comprehensive health checks...")
        
        checks = []
        
        # Basic health checks
        checks.append(await self.check_api_health())
        checks.append(await self.check_frontend_health())
        checks.append(await self.check_environment_configuration())
        checks.append(await self.check_data_quality())
        
        # Data source checks
        data_checks = await self.check_data_source_health()
        checks.extend(data_checks)
        
        # Store checks
        self.health_checks.extend(checks)
        
        # Keep only last 100 checks
        if len(self.health_checks) > 100:
            self.health_checks = self.health_checks[-100:]
        
        return checks
    
    def calculate_metrics(self) -> DeploymentMetrics:
        """Calculate deployment metrics."""
        if not self.health_checks:
            return DeploymentMetrics(
                total_checks=0,
                healthy_checks=0,
                warning_checks=0,
                critical_checks=0,
                average_response_time=0.0,
                uptime_percentage=0.0,
                last_check=datetime.now(),
                environment="production"
            )
        
        # Count statuses
        healthy_count = sum(1 for check in self.health_checks if check.status == "healthy")
        warning_count = sum(1 for check in self.health_checks if check.status == "warning")
        critical_count = sum(1 for check in self.health_checks if check.status == "critical")
        
        # Calculate average response time
        avg_response_time = sum(check.response_time for check in self.health_checks) / len(self.health_checks)
        
        # Calculate uptime percentage
        total_checks = len(self.health_checks)
        uptime_percentage = (healthy_count + warning_count) / total_checks if total_checks > 0 else 0.0
        
        return DeploymentMetrics(
            total_checks=total_checks,
            healthy_checks=healthy_count,
            warning_checks=warning_count,
            critical_checks=critical_count,
            average_response_time=avg_response_time,
            uptime_percentage=uptime_percentage,
            last_check=self.health_checks[-1].timestamp if self.health_checks else datetime.now(),
            environment="production"
        )
    
    def create_status_table(self, checks: List[HealthCheck]) -> Table:
        """Create status table for display."""
        table = Table(title="🚀 Deployment Health Status")
        
        table.add_column("Service", style="cyan", no_wrap=True)
        table.add_column("Status", style="bold")
        table.add_column("Response Time", style="green")
        table.add_column("Details", style="white")
        table.add_column("Timestamp", style="dim")
        
        for check in checks:
            # Color code status
            if check.status == "healthy":
                status_style = "green"
                status_icon = "✅"
            elif check.status == "warning":
                status_style = "yellow"
                status_icon = "⚠️"
            else:
                status_style = "red"
                status_icon = "❌"
            
            table.add_row(
                check.name,
                f"{status_icon} {check.status.upper()}",
                f"{check.response_time:.2f}s",
                check.details,
                check.timestamp.strftime("%H:%M:%S")
            )
        
        return table
    
    def create_metrics_panel(self, metrics: DeploymentMetrics) -> Panel:
        """Create metrics panel for display."""
        content = f"""
📊 **Deployment Metrics**
Total Checks: {metrics.total_checks}
Healthy: {metrics.healthy_checks} | Warning: {metrics.warning_checks} | Critical: {metrics.critical_checks}
Average Response Time: {metrics.average_response_time:.2f}s
Uptime: {metrics.uptime_percentage:.1%}
Last Check: {metrics.last_check.strftime('%H:%M:%S')}
Environment: {metrics.environment}
        """
        
        # Color based on uptime
        if metrics.uptime_percentage >= 0.95:
            style = "green"
        elif metrics.uptime_percentage >= 0.85:
            style = "yellow"
        else:
            style = "red"
        
        return Panel(content, title="📈 Performance Metrics", style=style)
    
    async def monitor_deployment(self, interval: int = 30):
        """Monitor deployment continuously."""
        logger.info(f"🚀 Starting deployment monitoring (interval: {interval}s)")
        
        with Live(
            Panel("Initializing monitoring...", title="🔄 Deployment Monitor"),
            refresh_per_second=4,
            console=self.console
        ) as live:
            
            while True:
                try:
                    # Run health checks
                    checks = await self.run_health_checks()
                    metrics = self.calculate_metrics()
                    
                    # Create display
                    status_table = self.create_status_table(checks)
                    metrics_panel = self.create_metrics_panel(metrics)
                    
                    # Combine display
                    display_content = f"{status_table}\n\n{metrics_panel}"
                    live.update(Panel(display_content, title="🚀 Real vs Test Data Deployment Monitor"))
                    
                    # Log summary
                    logger.info(f"Health Check Summary: {metrics.healthy_checks} healthy, {metrics.warning_checks} warnings, {metrics.critical_checks} critical")
                    
                    # Save metrics to file
                    self.save_metrics(metrics, checks)
                    
                    # Alert on critical issues
                    if metrics.critical_checks > 0:
                        logger.warning(f"🚨 CRITICAL ISSUES DETECTED: {metrics.critical_checks} critical checks")
                    
                    # Wait for next check
                    await asyncio.sleep(interval)
                    
                except Exception as e:
                    logger.error(f"Monitoring error: {e}")
                    live.update(Panel(f"❌ Monitoring Error: {e}", title="🚨 Error", style="red"))
                    await asyncio.sleep(interval)
    
    def save_metrics(self, metrics: DeploymentMetrics, checks: List[HealthCheck]):
        """Save metrics to file."""
        try:
            # Ensure logs directory exists
            Path("logs").mkdir(exist_ok=True)
            
            # Save metrics
            metrics_file = Path("logs/deployment_metrics.json")
            metrics_data = {
                "timestamp": datetime.now().isoformat(),
                "metrics": asdict(metrics),
                "checks": [asdict(check) for check in checks]
            }
            
            with open(metrics_file, 'w') as f:
                json.dump(metrics_data, f, indent=2, default=str)
                
        except Exception as e:
            logger.error(f"Error saving metrics: {e}")


async def main():
    """Main monitoring function."""
    monitor = DeploymentMonitor()
    
    console.print(Panel.fit(
        "🚀 Real vs Test Data Deployment Monitor\n"
        "High-level monitoring for production deployment",
        title="Deployment Monitor",
        style="blue"
    ))
    
    # Run monitoring
    await monitor.monitor_deployment(interval=30)


if __name__ == "__main__":
    asyncio.run(main()) 