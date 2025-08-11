#!/usr/bin/env python3
"""
Data Source Testing and Relevance Assessment
Tests all data sources and evaluates their relevance for Movember AI.
"""

import asyncio
import logging
import requests
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

console = Console()


@dataclass
class DataSourceTest:
    """Data source test result."""
    name: str
    endpoint: str
    status: str  # 'success', 'error', 'timeout'
    response_time: float
    data_quality: float
    relevance_score: float
    data_count: int
    last_updated: str
    details: str
    recommendations: List[str]


class DataSourceTester:
    """Test and evaluate data sources."""
    
    def __init__(self):
        self.api_base = "https://movember-api.onrender.com"
        self.test_results: List[DataSourceTest] = []
        
    async def test_grant_data_sources(self) -> List[DataSourceTest]:
        """Test grant-related data sources."""
        console.print("🔍 Testing Grant Data Sources...")
        
        tests = []
        
        # Test grant opportunities
        test = await self._test_endpoint(
            "Grant Opportunities",
            "/grant-acquisition/grant-opportunities/",
            "grants"
        )
        tests.append(test)
        
        # Test grant discovery
        test = await self._test_endpoint(
            "Grant Discovery",
            "/grant-acquisition/discover-grants/",
            "grants"
        )
        tests.append(test)
        
        # Test grant evaluation
        test = await self._test_endpoint(
            "Grant Evaluation",
            "/grant-evaluations/",
            "grants"
        )
        tests.append(test)
        
        return tests
    
    async def test_impact_data_sources(self) -> List[DataSourceTest]:
        """Test impact-related data sources."""
        console.print("📊 Testing Impact Data Sources...")
        
        tests = []
        
        # Test SROI calculation
        test = await self._test_endpoint(
            "SROI Calculation",
            "/impact-intelligence/calculate-sroi/",
            "impact"
        )
        tests.append(test)
        
        # Test impact measurement
        test = await self._test_endpoint(
            "Impact Measurement",
            "/impact-intelligence/measure-project-impact/",
            "impact"
        )
        tests.append(test)
        
        # Test impact reporting
        test = await self._test_endpoint(
            "Impact Reporting",
            "/impact-intelligence/generate-impact-report/",
            "impact"
        )
        tests.append(test)
        
        return tests
    
    async def test_research_data_sources(self) -> List[DataSourceTest]:
        """Test research-related data sources."""
        console.print("🔬 Testing Research Data Sources...")
        
        tests = []
        
        # Test external data
        test = await self._test_endpoint(
            "External Research Data",
            "/external-data/",
            "research"
        )
        tests.append(test)
        
        # Test AI grant assistant
        test = await self._test_endpoint(
            "AI Grant Assistant",
            "/ai-grant-assistant/",
            "research"
        )
        tests.append(test)
        
        return tests
    
    async def test_metrics_data_sources(self) -> List[DataSourceTest]:
        """Test metrics and analytics data sources."""
        console.print("📈 Testing Metrics Data Sources...")
        
        tests = []
        
        # Test success analytics
        test = await self._test_endpoint(
            "Success Analytics",
            "/grant-acquisition/success-analytics/",
            "metrics"
        )
        tests.append(test)
        
        # Test success tracking
        test = await self._test_endpoint(
            "Success Tracking",
            "/grant-acquisition/track-success/",
            "metrics"
        )
        tests.append(test)
        
        # Test success strategy
        test = await self._test_endpoint(
            "Success Strategy",
            "/grant-acquisition/success-strategy/",
            "metrics"
        )
        tests.append(test)
        
        return tests
    
    async def _test_endpoint(self, name: str, endpoint: str, data_type: str) -> DataSourceTest:
        """Test a specific endpoint."""
        start_time = datetime.now()
        
        try:
            response = requests.get(f"{self.api_base}{endpoint}", timeout=15)
            response_time = (datetime.now() - start_time).total_seconds()
            
            if response.status_code == 200:
                data = response.json()
                
                # Analyze data quality and relevance
                data_quality = self._assess_data_quality(data, data_type)
                relevance_score = self._assess_relevance(data, data_type)
                data_count = self._count_data_items(data)
                last_updated = data.get('timestamp', datetime.now().isoformat())
                
                status = "success"
                details = f"HTTP {response.status_code}, {data_count} items"
                recommendations = self._generate_recommendations(data, data_type, relevance_score)
                
            else:
                status = "error"
                data_quality = 0.0
                relevance_score = 0.0
                data_count = 0
                last_updated = datetime.now().isoformat()
                details = f"HTTP {response.status_code}"
                recommendations = ["Check endpoint configuration", "Verify data source availability"]
                
        except requests.exceptions.Timeout:
            status = "timeout"
            response_time = 15.0
            data_quality = 0.0
            relevance_score = 0.0
            data_count = 0
            last_updated = datetime.now().isoformat()
            details = "Request timeout"
            recommendations = ["Increase timeout", "Check network connectivity"]
            
        except Exception as e:
            status = "error"
            response_time = (datetime.now() - start_time).total_seconds()
            data_quality = 0.0
            relevance_score = 0.0
            data_count = 0
            last_updated = datetime.now().isoformat()
            details = str(e)
            recommendations = ["Check endpoint availability", "Verify API configuration"]
        
        return DataSourceTest(
            name=name,
            endpoint=endpoint,
            status=status,
            response_time=response_time,
            data_quality=data_quality,
            relevance_score=relevance_score,
            data_count=data_count,
            last_updated=last_updated,
            details=details,
            recommendations=recommendations
        )
    
    def _assess_data_quality(self, data: Dict[str, Any], data_type: str) -> float:
        """Assess data quality score."""
        score = 0.0
        total_checks = 0
        
        # Check for required fields
        if data_type == "grants":
            required_fields = ['status', 'opportunities', 'total_opportunities']
            for field in required_fields:
                total_checks += 1
                if field in data:
                    score += 1.0
        
        elif data_type == "impact":
            required_fields = ['status', 'impact_metrics', 'sroi_score']
            for field in required_fields:
                total_checks += 1
                if field in data:
                    score += 1.0
        
        elif data_type == "research":
            required_fields = ['status', 'research_data', 'publications']
            for field in required_fields:
                total_checks += 1
                if field in data:
                    score += 1.0
        
        elif data_type == "metrics":
            required_fields = ['status', 'analytics', 'success_rate']
            for field in required_fields:
                total_checks += 1
                if field in data:
                    score += 1.0
        
        # Check data freshness
        if 'timestamp' in data:
            total_checks += 1
            score += 1.0
        
        # Check data structure
        if isinstance(data, dict) and len(data) > 0:
            total_checks += 1
            score += 1.0
        
        return score / total_checks if total_checks > 0 else 0.0
    
    def _assess_relevance(self, data: Dict[str, Any], data_type: str) -> float:
        """Assess relevance score for Movember AI."""
        score = 0.0
        total_checks = 0
        
        # Check for Movember-specific content
        movember_keywords = ['men', 'health', 'prostate', 'testicular', 'mental', 'suicide', 'movember']
        data_str = json.dumps(data).lower()
        
        for keyword in movember_keywords:
            total_checks += 1
            if keyword in data_str:
                score += 1.0
        
        # Check for grant-related content
        if data_type == "grants":
            grant_keywords = ['grant', 'funding', 'opportunity', 'application', 'budget']
            for keyword in grant_keywords:
                total_checks += 1
                if keyword in data_str:
                    score += 1.0
        
        # Check for impact-related content
        elif data_type == "impact":
            impact_keywords = ['impact', 'outcome', 'measurement', 'sroi', 'evaluation']
            for keyword in impact_keywords:
                total_checks += 1
                if keyword in data_str:
                    score += 1.0
        
        # Check for research-related content
        elif data_type == "research":
            research_keywords = ['research', 'study', 'publication', 'evidence', 'analysis']
            for keyword in research_keywords:
                total_checks += 1
                if keyword in data_str:
                    score += 1.0
        
        # Check for metrics-related content
        elif data_type == "metrics":
            metrics_keywords = ['analytics', 'metrics', 'performance', 'success', 'tracking']
            for keyword in metrics_keywords:
                total_checks += 1
                if keyword in data_str:
                    score += 1.0
        
        return score / total_checks if total_checks > 0 else 0.0
    
    def _count_data_items(self, data: Dict[str, Any]) -> int:
        """Count data items in response."""
        if 'opportunities' in data:
            return len(data['opportunities'])
        elif 'data' in data:
            return len(data['data']) if isinstance(data['data'], list) else 1
        elif 'results' in data:
            return len(data['results'])
        else:
            return 1
    
    def _generate_recommendations(self, data: Dict[str, Any], data_type: str, relevance_score: float) -> List[str]:
        """Generate recommendations for improving data source relevance."""
        recommendations = []
        
        if relevance_score < 0.5:
            recommendations.append("Increase Movember-specific content")
            recommendations.append("Add more men's health related data")
        
        if data_type == "grants" and relevance_score < 0.7:
            recommendations.append("Include more health-focused grant opportunities")
            recommendations.append("Add prostate and testicular cancer research grants")
        
        if data_type == "impact" and relevance_score < 0.7:
            recommendations.append("Include more men's health impact metrics")
            recommendations.append("Add mental health and suicide prevention outcomes")
        
        if data_type == "research" and relevance_score < 0.7:
            recommendations.append("Include more men's health research publications")
            recommendations.append("Add recent studies on prostate cancer and mental health")
        
        if data_type == "metrics" and relevance_score < 0.7:
            recommendations.append("Include more health-focused success metrics")
            recommendations.append("Add grant success rates for health projects")
        
        return recommendations
    
    def create_results_table(self, tests: List[DataSourceTest]) -> Table:
        """Create results table."""
        table = Table(title="📊 Data Source Test Results")
        
        table.add_column("Data Source", style="cyan", no_wrap=True)
        table.add_column("Status", style="bold")
        table.add_column("Response Time", style="green")
        table.add_column("Quality", style="blue")
        table.add_column("Relevance", style="yellow")
        table.add_column("Data Count", style="magenta")
        
        for test in tests:
            # Status icon
            if test.status == "success":
                status_icon = "✅"
            elif test.status == "timeout":
                status_icon = "⏰"
            else:
                status_icon = "❌"
            
            # Color relevance score
            if test.relevance_score >= 0.8:
                relevance_style = "green"
            elif test.relevance_score >= 0.6:
                relevance_style = "yellow"
            else:
                relevance_style = "red"
            
            table.add_row(
                test.name,
                f"{status_icon} {test.status.upper()}",
                f"{test.response_time:.2f}s",
                f"{test.data_quality:.1%}",
                f"{test.relevance_score:.1%}",
                str(test.data_count)
            )
        
        return table
    
    def create_recommendations_panel(self, tests: List[DataSourceTest]) -> Panel:
        """Create recommendations panel."""
        recommendations = []
        
        for test in tests:
            if test.recommendations:
                recommendations.append(f"**{test.name}:**")
                for rec in test.recommendations:
                    recommendations.append(f"  • {rec}")
                recommendations.append("")
        
        if not recommendations:
            recommendations = ["All data sources are performing well!"]
        
        content = "\n".join(recommendations)
        return Panel(content, title="💡 Recommendations for Improvement", style="blue")
    
    async def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run comprehensive data source testing."""
        console.print(Panel.fit(
            "🔍 Data Source Testing and Relevance Assessment\n"
            "Evaluating all data sources for Movember AI relevance",
            title="Data Source Tester",
            style="blue"
        ))
        
        all_tests = []
        
        # Test all data source types
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            task = progress.add_task("Testing data sources...", total=4)
            
            # Test grant sources
            grant_tests = await self.test_grant_data_sources()
            all_tests.extend(grant_tests)
            progress.update(task, advance=1)
            
            # Test impact sources
            impact_tests = await self.test_impact_data_sources()
            all_tests.extend(impact_tests)
            progress.update(task, advance=1)
            
            # Test research sources
            research_tests = await self.test_research_data_sources()
            all_tests.extend(research_tests)
            progress.update(task, advance=1)
            
            # Test metrics sources
            metrics_tests = await self.test_metrics_data_sources()
            all_tests.extend(metrics_tests)
            progress.update(task, advance=1)
        
        # Calculate summary statistics
        successful_tests = [t for t in all_tests if t.status == "success"]
        avg_quality = sum(t.data_quality for t in successful_tests) / len(successful_tests) if successful_tests else 0
        avg_relevance = sum(t.relevance_score for t in successful_tests) / len(successful_tests) if successful_tests else 0
        avg_response_time = sum(t.response_time for t in successful_tests) / len(successful_tests) if successful_tests else 0
        
        # Display results
        console.print(self.create_results_table(all_tests))
        console.print(self.create_recommendations_panel(all_tests))
        
        # Create summary
        summary = {
            "total_tests": len(all_tests),
            "successful_tests": len(successful_tests),
            "success_rate": len(successful_tests) / len(all_tests) if all_tests else 0,
            "average_quality": avg_quality,
            "average_relevance": avg_relevance,
            "average_response_time": avg_response_time,
            "tests": [vars(t) for t in all_tests]
        }
        
        # Display summary
        summary_panel = Panel(
            f"📊 **Test Summary**\n"
            f"Total Tests: {summary['total_tests']}\n"
            f"Successful: {summary['successful_tests']} ({summary['success_rate']:.1%})\n"
            f"Average Quality: {summary['average_quality']:.1%}\n"
            f"Average Relevance: {summary['average_relevance']:.1%}\n"
            f"Average Response Time: {summary['average_response_time']:.2f}s",
            title="📈 Test Results Summary",
            style="green" if summary['success_rate'] >= 0.8 else "yellow"
        )
        console.print(summary_panel)
        
        return summary


async def main():
    """Main function."""
    tester = DataSourceTester()
    results = await tester.run_comprehensive_test()
    
    # Save results
    with open('data_source_test_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    console.print("💾 Results saved to data_source_test_results.json")


if __name__ == "__main__":
    asyncio.run(main()) 