#!/usr/bin/env python3
"""
Test script for Phase 1: Foundation Enhancement
Tests caching, performance monitoring, and enhanced metrics
"""

import asyncio
import time
from datetime import datetime
from rules.core.cache import get_rule_cache, CacheStrategy
from monitoring.advanced_metrics import get_metrics_collector, PerformanceMetric

async def test_rule_caching():
    """Test the rule caching system."""
    print("🧪 Testing Rule Caching System...")

    cache = get_rule_cache()

    # Test data
    test_context = {
        "context_type": "impact_reporting",
        "data": {"title": "Test Report", "content": "Test content"}
    }

    # Test cache miss
    result = await cache.get("test_rule", test_context)
    assert result is None, "Cache should be empty initially"

    # Test cache set and get
    test_result = {"status": "success", "score": 8.5}
    await cache.set("test_rule", test_context, test_result)

    cached_result = await cache.get("test_rule", test_context)
    assert cached_result == test_result, "Cached result should match"

    # Test cache stats
    stats = cache.get_stats()
    assert stats["hits"] >= 1, "Should have at least one cache hit"
    assert stats["cache_size"] >= 1, "Should have at least one cached entry"

    print("✅ Rule caching system working correctly")

async def test_performance_monitoring():
    """Test the performance monitoring system."""
    print("🧪 Testing Performance Monitoring System...")

    metrics = get_metrics_collector()

    # Record some test metrics
    await metrics.record_performance_metric(
        PerformanceMetric(
            timestamp=datetime.now(),
            metric_name="test_response_time",
            value=150.5,
            unit="milliseconds",
            category="api_performance",
            context={"endpoint": "/test/", "method": "GET"}
        )
    )

    # Get real-time metrics
    real_time_metrics = await metrics.get_real_time_metrics()
    assert "system_health" in real_time_metrics, "Should have system health data"
    assert "recent_metrics" in real_time_metrics, "Should have recent metrics"

    # Get performance summary
    summary = await metrics.get_performance_summary(hours=1)
    assert "metrics_summary" in summary, "Should have metrics summary"
    assert "health_summary" in summary, "Should have health summary"

    print("✅ Performance monitoring system working correctly")

async def test_system_health():
    """Test system health collection."""
    print("🧪 Testing System Health Collection...")

    metrics = get_metrics_collector()

    # Collect system health
    health = await metrics.collect_system_metrics()

    # Verify health data structure
    assert hasattr(health, 'cpu_usage'), "Should have CPU usage"
    assert hasattr(health, 'memory_usage'), "Should have memory usage"
    assert hasattr(health, 'disk_usage'), "Should have disk usage"
    assert hasattr(health, 'uptime'), "Should have uptime"

    # Verify reasonable values
    assert 0 <= health.cpu_usage <= 100, "CPU usage should be 0-100%"
    assert 0 <= health.memory_usage <= 100, "Memory usage should be 0-100%"
    assert 0 <= health.disk_usage <= 100, "Disk usage should be 0-100%"

    print("✅ System health collection working correctly")

async def test_cache_optimization():
    """Test cache optimization features."""
    print("🧪 Testing Cache Optimization...")

    cache = get_rule_cache()

    # Set cache to adaptive strategy
    cache.strategy = CacheStrategy.ADAPTIVE

    # Add some test data
    test_contexts = [
        {"context_type": "impact_reporting", "data": {"id": 1}},
        {"context_type": "grant_lifecycle", "data": {"id": 2}},
        {"context_type": "ai_behaviour", "data": {"id": 3}}
    ]

    for i, context in enumerate(test_contexts):
        await cache.set(f"test_rule_{i}", context, {"result": f"test_{i}"})

    # Test optimization
    optimization = await cache.optimize()
    assert "suggestions" in optimization, "Should have optimization suggestions"

    print("✅ Cache optimization working correctly")

async def test_performance_improvements():
    """Test performance improvements."""
    print("🧪 Testing Performance Improvements...")

    cache = get_rule_cache()
    metrics = get_metrics_collector()

    # Test cache hit performance
    test_context = {"context_type": "test", "data": {"test": True}}

    # First call (cache miss)
    start_time = time.time()
    result1 = await cache.get("performance_test", test_context)
    miss_time = time.time() - start_time

    # Set cache
    await cache.set("performance_test", test_context, {"result": "test"})

    # Second call (cache hit)
    start_time = time.time()
    result2 = await cache.get("performance_test", test_context)
    hit_time = time.time() - start_time

    # Cache hit should be faster
    assert hit_time < miss_time, "Cache hit should be faster than cache miss"

    print(f"✅ Performance improvement verified: Cache hit {hit_time:.4f}s vs miss {miss_time:.4f}s")

async def main():
    """Run all Phase 1 enhancement tests."""
    print("🚀 Phase 1: Foundation Enhancement Tests")
    print("=" * 50)

    try:
        await test_rule_caching()
        await test_performance_monitoring()
        await test_system_health()
        await test_cache_optimization()
        await test_performance_improvements()

        print("\n🎉 All Phase 1 enhancement tests passed!")
        print("\n📊 Phase 1 Success Metrics:")
        print("✅ Rule caching system implemented")
        print("✅ Performance monitoring operational")
        print("✅ System health collection working")
        print("✅ Cache optimization features active")
        print("✅ Performance improvements verified")

    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
