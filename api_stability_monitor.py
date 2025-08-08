#!/usr/bin/env python3
"""
API Stability Monitor
Monitors the Movember API endpoints for stability issues.
"""

import asyncio
import time
import httpx
import logging
from datetime import datetime
from typing import Dict, List, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIStabilityMonitor:


    """Monitors API stability and identifies issues."""

    def __init__(self, base_url: str = "http://localhost:8001"):


        self.base_url = base_url
        self.endpoints = [
            "/health/",
            "/data-upload/health/",
            "/real-data/health/",
            "/grant-acquisition/health/",
            "/impact-intelligence/health/",
            "/logo/",
            "/favicon.ico"
        ]
        self.results = []

    async def test_endpoint(self, endpoint: str) -> Dict[str, Any]:
        """Test a single endpoint."""
        start_time = time.time()
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.base_url}{endpoint}")
                response_time = time.time() - start_time

                return {
                    "endpoint": endpoint,
                    "status_code": response.status_code,
                    "response_time": response_time,
                    "success": response.status_code == 200,
                    "timestamp": datetime.now().isoformat(),
                    "error": None
                }
        except Exception as e:
            response_time = time.time() - start_time
            return {
                "endpoint": endpoint,
                "status_code": None,
                "response_time": response_time,
                "success": False,
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }

    async def run_stability_test(self, duration: int = 60, interval: float = 5.0) -> Dict[str, Any]:
        """Run a stability test for the specified duration."""
        logger.info(f"Starting API stability test for {duration} seconds...")

        start_time = time.time()
        test_results = []

        while time.time() - start_time < duration:
            batch_results = []

            # Test all endpoints concurrently
            tasks = [self.test_endpoint(endpoint) for endpoint in self.endpoints]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, dict):
                    batch_results.append(result)
                else:
                    batch_results.append({
                        "endpoint": "unknown",
                        "status_code": None,
                        "response_time": 0,
                        "success": False,
                        "timestamp": datetime.now().isoformat(),
                        "error": str(result)
                    })

            test_results.append({
                "batch": len(test_results) + 1,
                "timestamp": datetime.now().isoformat(),
                "results": batch_results
            })

            # Log current status
            successful = sum(1 for r in batch_results if r["success"])
            total = len(batch_results)
            logger.info(f"Batch {len(test_results)}: {successful}/{total} endpoints successful")

            await asyncio.sleep(interval)

        return self.analyze_results(test_results)

    def analyze_results(self, test_results: List[Dict[str, Any]]) -> Dict[str, Any]:


        """Analyze test results for stability issues."""
        total_requests = 0
        successful_requests = 0
        failed_requests = 0
        endpoint_stats = {}

        for batch in test_results:
            for result in batch["results"]:
                total_requests += 1
                endpoint = result["endpoint"]

                if endpoint not in endpoint_stats:
                    endpoint_stats[endpoint] = {
                        "total": 0,
                        "successful": 0,
                        "failed": 0,
                        "avg_response_time": 0,
                        "errors": []
                    }

                endpoint_stats[endpoint]["total"] += 1

                if result["success"]:
                    successful_requests += 1
                    endpoint_stats[endpoint]["successful"] += 1
                else:
                    failed_requests += 1
                    endpoint_stats[endpoint]["failed"] += 1
                    if result["error"]:
                        endpoint_stats[endpoint]["errors"].append(result["error"])

                # Update average response time
                current_avg = endpoint_stats[endpoint]["avg_response_time"]
                current_count = endpoint_stats[endpoint]["successful"]
                if current_count > 0:
                    new_avg = ((current_avg * (current_count - 1)) + result["response_time"]) / current_count
                    endpoint_stats[endpoint]["avg_response_time"] = new_avg

        # Calculate overall statistics
        success_rate = (successful_requests / total_requests * 100) if total_requests > 0 else 0

        # Identify problematic endpoints
        problematic_endpoints = []
        for endpoint, stats in endpoint_stats.items():
            if stats["failed"] > 0:
                failure_rate = (stats["failed"] / stats["total"]) * 100
                problematic_endpoints.append({
                    "endpoint": endpoint,
                    "failure_rate": failure_rate,
                    "total_requests": stats["total"],
                    "failed_requests": stats["failed"],
                    "errors": stats["errors"]
                })

        return {
            "test_duration": len(test_results) * 5,  # 5 second intervals
            "total_requests": total_requests,
            "successful_requests": successful_requests,
            "failed_requests": failed_requests,
            "success_rate": success_rate,
            "endpoint_stats": endpoint_stats,
            "problematic_endpoints": problematic_endpoints,
            "recommendations": self.generate_recommendations(success_rate, problematic_endpoints)
        }

    def generate_recommendations(self, success_rate: float, problematic_endpoints: List[Dict[str, Any]]) -> List[str]:


        """Generate recommendations based on test results."""
        recommendations = []

        if success_rate < 95:
            recommendations.append("⚠️ Overall API stability is below 95% - investigate root cause")

        if problematic_endpoints:
            recommendations.append(f"🔧 {len(problematic_endpoints)} endpoints have stability issues")
            for endpoint in problematic_endpoints:
                recommendations.append(f"  - {endpoint['endpoint']}: {endpoint['failure_rate']:.1f}% failure rate")

        if success_rate >= 99:
            recommendations.append("✅ API stability is excellent")

        return recommendations

async def main():
    """Run the API stability monitor."""
    monitor = APIStabilityMonitor()

    print("🔍 Movember API Stability Monitor")
    print("=" * 50)

    # Quick health check first
    print("\n📊 Quick Health Check:")
    quick_results = await asyncio.gather(*[
        monitor.test_endpoint(endpoint) for endpoint in monitor.endpoints
    ])

    for result in quick_results:
        status = "✅" if result["success"] else "❌"
        print(f"{status} {result['endpoint']}: {result['status_code']} ({result['response_time']:.3f}s)")

    # Run stability test
    print(f"\n🔄 Running 60-second stability test...")
    analysis = await monitor.run_stability_test(duration=60, interval=5.0)

    print("\n📈 Stability Analysis:")
    print(f"Total Requests: {analysis['total_requests']}")
    print(f"Successful: {analysis['successful_requests']}")
    print(f"Failed: {analysis['failed_requests']}")
    print(f"Success Rate: {analysis['success_rate']:.2f}%")

    if analysis['problematic_endpoints']:
        print("\n⚠️ Problematic Endpoints:")
        for endpoint in analysis['problematic_endpoints']:
            print(f"  - {endpoint['endpoint']}: {endpoint['failure_rate']:.1f}% failure rate")

    print("\n💡 Recommendations:")
    for recommendation in analysis['recommendations']:
        print(f"  {recommendation}")

if __name__ == "__main__":
    asyncio.run(main())
