#!/usr/bin/env python3
"""
Health Monitor for Movember AI Rules System
Monitors API health and tracks intermittent errors.
"""

import asyncio
import logging
import time
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
from dataclasses import dataclass
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
console = Console()

@dataclass
class HealthCheck:
    """Health check result."""
    timestamp: datetime
    status_code: int
    response_time: float
    system_status: str = "unknown"
    active_rules: int = 0
    error_count: int = 0
    error_message: str = ""

class HealthMonitor:
    """Monitor API health and track intermittent errors."""
    
    def __init__(self, api_url: str = "https://movember-api.onrender.com"):
        self.api_url = api_url
        self.health_checks: List[HealthCheck] = []
        self.error_count = 0
        self.success_count = 0
        self.start_time = datetime.now()
    
    async def check_health(self) -> HealthCheck:
        """Perform a single health check."""
        start_time = time.time()
        
        try:
            response = requests.get(f"{self.api_url}/health/", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                return HealthCheck(
                    timestamp=datetime.now(),
                    status_code=response.status_code,
                    response_time=response_time,
                    system_status=data.get("system_status", "unknown"),
                    active_rules=data.get("active_rules", 0),
                    error_count=data.get("error_count", 0)
                )
            else:
                return HealthCheck(
                    timestamp=datetime.now(),
                    status_code=response.status_code,
                    response_time=response_time,
                    error_message=f"HTTP {response.status_code}"
                )
                
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheck(
                timestamp=datetime.now(),
                status_code=500,
                response_time=response_time,
                error_message=str(e)
            )
    
    async def monitor_continuously(self, interval: int = 30):
        """Monitor health continuously."""
        console.print(Panel.fit(
            f"[bold blue]Movember AI Rules System Health Monitor[/bold blue]\n"
            f"Monitoring: {self.api_url}\n"
            f"Interval: {interval} seconds",
            title="Health Monitor Started"
        ))
        
        with Live(self._create_status_table(), refresh_per_second=1) as live:
            while True:
                try:
                    # Perform health check
                    health_check = await self.check_health()
                    self.health_checks.append(health_check)
                    
                    # Update counters
                    if health_check.status_code == 200:
                        self.success_count += 1
                    else:
                        self.error_count += 1
                    
                    # Keep only last 100 checks
                    if len(self.health_checks) > 100:
                        self.health_checks = self.health_checks[-100:]
                    
                    # Update display
                    live.update(self._create_status_table())
                    
                    # Log errors
                    if health_check.status_code != 200:
                        logger.warning(f"Health check failed: {health_check.error_message}")
                    
                    await asyncio.sleep(interval)
                    
                except KeyboardInterrupt:
                    console.print("\n[bold red]Monitoring stopped by user[/bold red]")
                    break
                except Exception as e:
                    logger.error(f"Monitor error: {str(e)}")
                    await asyncio.sleep(interval)
    
    def _create_status_table(self) -> Table:
        """Create status table for display."""
        table = Table(title="Movember AI Rules System - Health Status")
        
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        table.add_column("Details", style="yellow")
        
        # Current status
        if self.health_checks:
            latest = self.health_checks[-1]
            status_emoji = "✅" if latest.status_code == 200 else "❌"
            table.add_row(
                "Current Status",
                f"{status_emoji} {latest.system_status.upper()}",
                f"HTTP {latest.status_code} ({latest.response_time:.3f}s)"
            )
        
        # Uptime
        uptime = datetime.now() - self.start_time
        table.add_row(
            "Uptime",
            f"{uptime.total_seconds():.0f}s",
            f"Started: {self.start_time.strftime('%H:%M:%S')}"
        )
        
        # Success rate
        total_checks = self.success_count + self.error_count
        if total_checks > 0:
            success_rate = (self.success_count / total_checks) * 100
            table.add_row(
                "Success Rate",
                f"{success_rate:.1f}%",
                f"{self.success_count}/{total_checks} checks"
            )
        
        # Recent errors
        recent_errors = [h for h in self.health_checks[-10:] if h.status_code != 200]
        if recent_errors:
            table.add_row(
                "Recent Errors",
                f"{len(recent_errors)}",
                f"Last: {recent_errors[-1].timestamp.strftime('%H:%M:%S')}"
            )
        else:
            table.add_row(
                "Recent Errors",
                "0",
                "All recent checks successful"
            )
        
        # System metrics
        if self.health_checks and self.health_checks[-1].status_code == 200:
            latest = self.health_checks[-1]
            table.add_row(
                "Active Rules",
                str(latest.active_rules),
                "Rules engine operational"
            )
            table.add_row(
                "Error Count",
                str(latest.error_count),
                "System error count"
            )
        
        return table
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate a health report."""
        if not self.health_checks:
            return {"error": "No health checks performed"}
        
        total_checks = len(self.health_checks)
        successful_checks = len([h for h in self.health_checks if h.status_code == 200])
        failed_checks = total_checks - successful_checks
        
        recent_checks = self.health_checks[-10:]
        recent_success_rate = len([h for h in recent_checks if h.status_code == 200]) / len(recent_checks) * 100
        
        avg_response_time = sum(h.response_time for h in self.health_checks) / total_checks
        
        return {
            "monitoring_started": self.start_time.isoformat(),
            "total_checks": total_checks,
            "successful_checks": successful_checks,
            "failed_checks": failed_checks,
            "overall_success_rate": (successful_checks / total_checks) * 100 if total_checks > 0 else 0,
            "recent_success_rate": recent_success_rate,
            "average_response_time": avg_response_time,
            "last_check": self.health_checks[-1].timestamp.isoformat(),
            "last_status": self.health_checks[-1].system_status if self.health_checks[-1].status_code == 200 else "error",
            "last_status_code": self.health_checks[-1].status_code
        }

async def main():
    """Main monitoring function."""
    monitor = HealthMonitor()
    
    try:
        await monitor.monitor_continuously(interval=30)
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Generating final report...[/bold yellow]")
        report = monitor.generate_report()
        console.print(Panel(json.dumps(report, indent=2), title="Final Health Report"))

if __name__ == "__main__":
    asyncio.run(main()) 