#!/usr/bin/env python3
"""
Phase 2 Implementation Test
Tests the five high-priority data sources and measures relevance improvement.
"""
import asyncio
import logging
import json
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass

# Import Phase 2 data sources
from data.sources.pubmed_source import PubMedDataSource
from data.sources.grants_gov_source import GrantsGovDataSource
from data.sources.nhmrc_source import NHMRCDataSource
from data.sources.beyond_blue_source import BeyondBlueDataSource
from data.sources.arc_source import ARCDataSource

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Phase2TestResult:
    """Phase 2 test result data structure."""
    source_name: str
    connection_status: str
    response_time: float
    data_items_retrieved: int
    relevance_score: float
    data_quality: float
    error_message: str = None

class Phase2ImplementationTester:
    """Test Phase 2 data source implementation."""
    
    def __init__(self):
        self.sources = {
            "PubMed Central": PubMedDataSource(),
            "Grants.gov": GrantsGovDataSource(),
            "NHMRC": NHMRCDataSource(),
            "Beyond Blue": BeyondBlueDataSource(),
            "Australian Research Council": ARCDataSource()
        }
        self.results = []
        
    async def test_all_sources(self) -> List[Phase2TestResult]:
        """Test all Phase 2 data sources."""
        logger.info("🚀 Starting Phase 2 Implementation Testing")
        
        for source_name, source in self.sources.items():
            logger.info(f"Testing {source_name}...")
            result = await self._test_source(source_name, source)
            self.results.append(result)
            
        return self.results
    
    async def _test_source(self, source_name: str, source) -> Phase2TestResult:
        """Test a single data source."""
        try:
            start_time = datetime.now()
            
            # Test connection
            connection_result = await source.test_connection()
            
            response_time = (datetime.now() - start_time).total_seconds()
            
            if connection_result["status"] == "success":
                return Phase2TestResult(
                    source_name=source_name,
                    connection_status="success",
                    response_time=response_time,
                    data_items_retrieved=connection_result.get("studies_retrieved", 0) + 
                                        connection_result.get("opportunities_retrieved", 0) +
                                        connection_result.get("projects_retrieved", 0) +
                                        connection_result.get("statistics_retrieved", 0),
                    relevance_score=connection_result.get("relevance_score", 0.0),
                    data_quality=connection_result.get("data_quality", 0.0)
                )
            else:
                return Phase2TestResult(
                    source_name=source_name,
                    connection_status="error",
                    response_time=response_time,
                    data_items_retrieved=0,
                    relevance_score=0.0,
                    data_quality=0.0,
                    error_message=connection_result.get("error", "Unknown error")
                )
                
        except Exception as e:
            logger.error(f"Error testing {source_name}: {str(e)}")
            return Phase2TestResult(
                source_name=source_name,
                connection_status="error",
                response_time=0.0,
                data_items_retrieved=0,
                relevance_score=0.0,
                data_quality=0.0,
                error_message=str(e)
            )
    
    def calculate_overall_metrics(self) -> Dict[str, Any]:
        """Calculate overall Phase 2 metrics."""
        successful_tests = [r for r in self.results if r.connection_status == "success"]
        failed_tests = [r for r in self.results if r.connection_status == "error"]
        
        if not successful_tests:
            return {
                "success_rate": 0.0,
                "average_relevance": 0.0,
                "average_quality": 0.0,
                "total_data_items": 0,
                "average_response_time": 0.0
            }
        
        return {
            "success_rate": len(successful_tests) / len(self.results),
            "average_relevance": sum(r.relevance_score for r in successful_tests) / len(successful_tests),
            "average_quality": sum(r.data_quality for r in successful_tests) / len(successful_tests),
            "total_data_items": sum(r.data_items_retrieved for r in successful_tests),
            "average_response_time": sum(r.response_time for r in successful_tests) / len(successful_tests)
        }
    
    def generate_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report."""
        overall_metrics = self.calculate_overall_metrics()
        
        report = {
            "test_timestamp": datetime.now().isoformat(),
            "phase": "Phase 2 Implementation",
            "total_sources_tested": len(self.results),
            "successful_sources": len([r for r in self.results if r.connection_status == "success"]),
            "failed_sources": len([r for r in self.results if r.connection_status == "error"]),
            "overall_metrics": overall_metrics,
            "individual_results": [
                {
                    "source_name": r.source_name,
                    "connection_status": r.connection_status,
                    "response_time": r.response_time,
                    "data_items_retrieved": r.data_items_retrieved,
                    "relevance_score": r.relevance_score,
                    "data_quality": r.data_quality,
                    "error_message": r.error_message
                }
                for r in self.results
            ]
        }
        
        return report
    
    def print_test_summary(self):
        """Print test summary to console."""
        print("\n" + "="*80)
        print("🎯 PHASE 2 IMPLEMENTATION TEST RESULTS")
        print("="*80)
        
        overall_metrics = self.calculate_overall_metrics()
        
        print(f"\n📊 Overall Metrics:")
        print(f"   Success Rate: {overall_metrics['success_rate']:.1%}")
        print(f"   Average Relevance: {overall_metrics['average_relevance']:.1%}")
        print(f"   Average Quality: {overall_metrics['average_quality']:.1%}")
        print(f"   Total Data Items: {overall_metrics['total_data_items']}")
        print(f"   Average Response Time: {overall_metrics['average_response_time']:.3f}s")
        
        print(f"\n📋 Individual Results:")
        for result in self.results:
            status_icon = "✅" if result.connection_status == "success" else "❌"
            print(f"   {status_icon} {result.source_name}")
            print(f"      Status: {result.connection_status}")
            print(f"      Response Time: {result.response_time:.3f}s")
            print(f"      Data Items: {result.data_items_retrieved}")
            print(f"      Relevance: {result.relevance_score:.1%}")
            print(f"      Quality: {result.data_quality:.1%}")
            if result.error_message:
                print(f"      Error: {result.error_message}")
            print()
        
        print("="*80)

async def main():
    """Run Phase 2 implementation test."""
    tester = Phase2ImplementationTester()
    
    # Run tests
    results = await tester.test_all_sources()
    
    # Generate report
    report = tester.generate_test_report()
    
    # Print summary
    tester.print_test_summary()
    
    # Save report
    with open("PHASE2_TEST_REPORT.json", "w") as f:
        json.dump(report, f, indent=2)
    
    logger.info("Phase 2 implementation test completed!")
    logger.info(f"Test report saved to: PHASE2_TEST_REPORT.json")
    
    return report

if __name__ == "__main__":
    asyncio.run(main()) 