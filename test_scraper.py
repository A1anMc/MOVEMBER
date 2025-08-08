#!/usr/bin/env python3
"""
Test script for Movember Data Scraper
Demonstrates the scraping functionality
"""

import asyncio
import logging
from data_scraper import MovemberDataScraper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_scraper():
    """Test the data scraper functionality."""
    logger.info("🧪 Testing Movember Data Scraper...")

    # Create test configuration
    test_config = {
        "sources": [
            {
                "url": "https://httpbin.org/html",  # Test URL that returns HTML
                "selectors": {
                    "grant_container": "body",
                    "title": "h1",
                    "description": "p"
                }
            }
        ]
    }

    try:
        async with MovemberDataScraper() as scraper:
            logger.info("🕷️ Testing UK spelling conversion...")

            # Test UK spelling conversion
            test_text = "This uses American spelling like color and center and theater"
            uk_text = scraper.convert_to_uk_spelling(test_text)
            logger.info(f"Original: {test_text}")
            logger.info(f"UK Version: {uk_text}")

            logger.info("💰 Testing AUD currency formatting...")

            # Test currency formatting
            test_amount = 50000.00
            aud_formatted = scraper.format_aud_currency(test_amount)
            logger.info(f"Amount: {test_amount}")
            logger.info(f"AUD Formatted: {aud_formatted}")

            logger.info("🔍 Testing currency extraction...")

            # Test currency extraction
            test_text_with_currency = "This grant provides $25,000 USD for research"
            extracted_amount = scraper.extract_currency_amount(test_text_with_currency)
            logger.info(f"Text: {test_text_with_currency}")
            logger.info(f"Extracted Amount: {extracted_amount}")

            logger.info("📊 Testing data quality validation...")

            # Test data quality validation
            test_data = {
                "title": "Test Grant",
                "description": "This uses American spelling like color and center",
                "budget": 25000.00,
                "organisation": "Test University"
            }

            validated_data = scraper.validate_data_quality(test_data)
            logger.info(f"Quality Score: {validated_data.get('quality_score', 0)}%")
            logger.info(f"Quality Issues: {validated_data.get('quality_issues', [])}")

            logger.info("✅ Data scraper test completed successfully!")

    except Exception as e:
        logger.error(f"❌ Data scraper test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_scraper())
