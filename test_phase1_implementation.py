#!/usr/bin/env python3
"""
Phase 1 Implementation Test
Tests the three high-priority data sources and measures relevance improvement.
"""

import asyncio
import logging
import json
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# Import our new data sources
from data.sources.aihw_source import get_aihw_data, validate_aihw_connection
from data.sources.pcf_source import get_pcf_data, validate_pcf_connection
from data.sources.tcf_source import get_tcf_data, validate_tcf_connection

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

console = Console()


@dataclass
class Phase1TestResult:
    """Phase 1 test result."""
    data_source: str
    status: str
    relevance_score: float
    data_quality: Dict[str, float]
    response_time: float
    data_count: int
    connection_valid: bool
    details: str


class Phase1ImplementationTester:
    """Test Phase 1 data source implementations."""
    
    def __init__(self):
        self.test_results: List[Phase1TestResult] = []
        self.start_time = datetime.now()
        
    async def test_aihw_source(self) -> Phase1TestResult:
        """Test Australian Institute of Health and Welfare data source."""
        console.print("🔍 Testing AIHW Data Source...")
        
        start_time = datetime.now()
        
        try:
            # Test connection
            connection_valid = validate_aihw_connection()
            
            # Get data
            data = await get_aihw_data("all")
            
            response_time = (datetime.now() - start_time).total_seconds()
            
            if data["status"] == "success":
                relevance_score = data.get("relevance_score", 0.0)
                data_quality = data.get("data_quality", {})
                data_count = self._count_data_items(data.get("data", {}))
                
                return Phase1TestResult(
                    data_source="Australian Institute of Health and Welfare",
                    status="success",
                    relevance_score=relevance_score,
                    data_quality=data_quality,
                    response_time=response_time,
                    data_count=data_count,
                    connection_valid=connection_valid,
                    details=f"Successfully retrieved {data_count} data items"
                )
            else:
                return Phase1TestResult(
                    data_source="Australian Institute of Health and Welfare",
                    status="error",
                    relevance_score=0.0,
                    data_quality={},
                    response_time=response_time,
                    data_count=0,
                    connection_valid=connection_valid,
                    details=data.get("message", "Unknown error")
                )
                
        except Exception as e:
            response_time = (datetime.now() - start_time).total_seconds()
            return Phase1TestResult(
                data_source="Australian Institute of Health and Welfare",
                status="error",
                relevance_score=0.0,
                data_quality={},
                response_time=response_time,
                data_count=0,
                connection_valid=False,
                details=str(e)
            )
    
    async def test_pcf_source(self) -> Phase1TestResult:
        """Test Prostate Cancer Foundation data source."""
        console.print("🔍 Testing PCF Data Source...")
        
        start_time = datetime.now()
        
        try:
            # Test connection
            connection_valid = validate_pcf_connection()
            
            # Get data
            data = await get_pcf_data("all")
            
            response_time = (datetime.now() - start_time).total_seconds()
            
            if data["status"] == "success":
                relevance_score = data.get("relevance_score", 0.0)
                data_quality = data.get("data_quality", {})
                data_count = self._count_data_items(data.get("data", {}))
                
                return Phase1TestResult(
                    data_source="Prostate Cancer Foundation",
                    status="success",
                    relevance_score=relevance_score,
                    data_quality=data_quality,
                    response_time=response_time,
                    data_count=data_count,
                    connection_valid=connection_valid,
                    details=f"Successfully retrieved {data_count} data items"
                )
            else:
                return Phase1TestResult(
                    data_source="Prostate Cancer Foundation",
                    status="error",
                    relevance_score=0.0,
                    data_quality={},
                    response_time=response_time,
                    data_count=0,
                    connection_valid=connection_valid,
                    details=data.get("message", "Unknown error")
                )
                
        except Exception as e:
            response_time = (datetime.now() - start_time).total_seconds()
            return Phase1TestResult(
                data_source="Prostate Cancer Foundation",
                status="error",
                relevance_score=0.0,
                data_quality={},
                response_time=response_time,
                data_count=0,
                connection_valid=False,
                details=str(e)
            )
    
    async def test_tcf_source(self) -> Phase1TestResult:
        """Test Testicular Cancer Foundation data source."""
        console.print("🔍 Testing TCF Data Source...")
        
        start_time = datetime.now()
        
        try:
            # Test connection
            connection_valid = validate_tcf_connection()
            
            # Get data
            data = await get_tcf_data("all")
            
            response_time = (datetime.now() - start_time).total_seconds()
            
            if data["status"] == "success":
                relevance_score = data.get("relevance_score", 0.0)
                data_quality = data.get("data_quality", {})
                data_count = self._count_data_items(data.get("data", {}))
                
                return Phase1TestResult(
                    data_source="Testicular Cancer Foundation",
                    status="success",
                    relevance_score=relevance_score,
                    data_quality=data_quality,
                    response_time=response_time,
                    data_count=data_count,
                    connection_valid=connection_valid,
                    details=f"Successfully retrieved {data_count} data items"
                )
            else:
                return Phase1TestResult(
                    data_source="Testicular Cancer Foundation",
                    status="error",
                    relevance_score=0.0,
                    data_quality={},
                    response_time=response_time,
                    data_count=0,
                    connection_valid=connection_valid,
                    details=data.get("message", "Unknown error")
                )
                
        except Exception as e:
            response_time = (datetime.now() - start_time).total_seconds()
            return Phase1TestResult(
                data_source="Testicular Cancer Foundation",
                status="error",
                relevance_score=0.0,
                data_quality={},
                response_time=response_time,
                data_count=0,
                connection_valid=False,
                details=str(e)
            )
    
    def _count_data_items(self, data: Dict[str, Any]) -> int:
        """Count data items in response."""
        if not isinstance(data, dict):
            return 0
        
        count = 0
        for key, value in data.items():
            if isinstance(value, dict):
                count += len(value)
            elif isinstance(value, list):
                count += len(value)
            else:
                count += 1
        
        return count
    
    def create_results_table(self, results: List[Phase1TestResult]) -> Table:
        """Create results table."""
        table = Table(title="🚀 Phase 1 Implementation Test Results")
        
        table.add_column("Data Source", style="cyan", no_wrap=True)
        table.add_column("Status", style="bold")
        table.add_column("Relevance", style="yellow")
        table.add_column("Quality", style="blue")
        table.add_column("Response Time", style="green")
        table.add_column("Data Count", style="magenta")
        table.add_column("Connection", style="white")
        
        for result in results:
            # Status icon
            if result.status == "success":
                status_icon = "✅"
            else:
                status_icon = "❌"
            
            # Connection status
            if result.connection_valid:
                connection_icon = "✅"
            else:
                connection_icon = "❌"
            
            # Average quality score
            avg_quality = sum(result.data_quality.values()) / len(result.data_quality) if result.data_quality else 0.0
            
            table.add_row(
                result.data_source,
                f"{status_icon} {result.status.upper()}",
                f"{result.relevance_score:.1%}",
                f"{avg_quality:.1%}",
                f"{result.response_time:.2f}s",
                str(result.data_count),
                connection_icon
            )
        
        return table
    
    def create_improvement_panel(self, results: List[Phase1TestResult]) -> Panel:
        """Create improvement analysis panel."""
        successful_results = [r for r in results if r.status == "success"]
        
        if not successful_results:
            return Panel("No successful results to analyze", title="📊 Improvement Analysis", style="red")
        
        # Calculate metrics
        avg_relevance = sum(r.relevance_score for r in successful_results) / len(successful_results)
        avg_quality = sum(sum(r.data_quality.values()) / len(r.data_quality) for r in successful_results) / len(successful_results)
        avg_response_time = sum(r.response_time for r in successful_results) / len(successful_results)
        total_data_items = sum(r.data_count for r in successful_results)
        
        # Compare with previous results
        previous_avg_relevance = 0.306  # From our earlier analysis
        improvement = avg_relevance - previous_avg_relevance
        
        content = f"""
📊 **Phase 1 Implementation Results**

**Relevance Improvement:**
Previous Average: {previous_avg_relevance:.1%}
New Average: {avg_relevance:.1%}
Improvement: +{improvement:.1%} ({improvement/previous_avg_relevance:.1%} increase)

**Quality Metrics:**
Average Quality: {avg_quality:.1%}
Average Response Time: {avg_response_time:.2f}s
Total Data Items: {total_data_items}

**Implementation Status:**
Successful Sources: {len(successful_results)}/3
Connection Success Rate: {sum(1 for r in results if r.connection_valid)}/3
        """
        
        # Color based on improvement
        if improvement >= 0.3:
            style = "green"
        elif improvement >= 0.2:
            style = "yellow"
        else:
            style = "red"
        
        return Panel(content, title="📈 Relevance Improvement Analysis", style=style)
    
    async def run_phase1_tests(self) -> Dict[str, Any]:
        """Run all Phase 1 tests."""
        console.print(Panel.fit(
            "🚀 Phase 1 Implementation Testing\n"
            "Testing AIHW, PCF, and TCF data sources",
            title="Phase 1 Tester",
            style="blue"
        ))
        
        results = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            task = progress.add_task("Testing Phase 1 sources...", total=3)
            
            # Test AIHW
            aihw_result = await self.test_aihw_source()
            results.append(aihw_result)
            progress.update(task, advance=1)
            
            # Test PCF
            pcf_result = await self.test_pcf_source()
            results.append(pcf_result)
            progress.update(task, advance=1)
            
            # Test TCF
            tcf_result = await self.test_tcf_source()
            results.append(tcf_result)
            progress.update(task, advance=1)
        
        # Display results
        console.print(self.create_results_table(results))
        console.print(self.create_improvement_panel(results))
        
        # Create summary
        successful_results = [r for r in results if r.status == "success"]
        avg_relevance = sum(r.relevance_score for r in successful_results) / len(successful_results) if successful_results else 0.0
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_sources": len(results),
            "successful_sources": len(successful_results),
            "success_rate": len(successful_results) / len(results) if results else 0.0,
            "average_relevance": avg_relevance,
            "previous_average_relevance": 0.306,
            "improvement": avg_relevance - 0.306,
            "improvement_percentage": (avg_relevance - 0.306) / 0.306 if 0.306 > 0 else 0.0,
            "results": [vars(r) for r in results]
        }
        
        # Display summary
        summary_panel = Panel(
            f"🎯 **Phase 1 Implementation Summary**\n\n"
            f"Success Rate: {summary['success_rate']:.1%}\n"
            f"Average Relevance: {summary['average_relevance']:.1%}\n"
            f"Improvement: +{summary['improvement']:.1%} ({summary['improvement_percentage']:.1%} increase)\n\n"
            f"✅ **Phase 1 Implementation: {'SUCCESS' if summary['success_rate'] >= 0.8 else 'NEEDS ATTENTION'}**",
            title="📋 Test Summary",
            style="green" if summary['success_rate'] >= 0.8 else "yellow"
        )
        console.print(summary_panel)
        
        return summary


async def main():
    """Main function."""
    tester = Phase1ImplementationTester()
    results = await tester.run_phase1_tests()
    
    # Save results
    with open('phase1_implementation_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    console.print("💾 Results saved to phase1_implementation_results.json")


if __name__ == "__main__":
    # Import dataclass
    from dataclasses import dataclass
    
    asyncio.run(main()) 