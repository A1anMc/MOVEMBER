#!/usr/bin/env python3
"""
Test script for Movember Monitoring Bot
Demonstrates the monitoring functionality
"""

import asyncio
import logging
from monitoring_bot import MovemberMonitoringBot

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_monitoring():
    """Test the monitoring bot functionality."""
    logger.info("🧪 Testing Movember Monitoring Bot...")

    # Create monitoring bot
    bot = MovemberMonitoringBot(check_interval=5)  # Short interval for testing

    try:
        # Run one monitoring cycle
        logger.info("🏥 Running health checks...")
        await bot.run_health_checks()

        logger.info("📊 Checking data quality...")
        await bot.check_data_quality()

        logger.info("🔍 Validating compliance...")
        await bot.validate_compliance()

        logger.info("📈 Collecting system metrics...")
        await bot.collect_system_metrics()

        logger.info("🚨 Generating alerts...")
        await bot.generate_alerts()

        logger.info("✅ Monitoring test completed successfully!")

    except Exception as e:
        logger.error(f"❌ Monitoring test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_monitoring())
