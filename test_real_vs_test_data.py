#!/usr/bin/env python3
"""
Test Real vs Test Data Implementation
Validates the environment configuration, data source factory, and quality validation.
"""

import asyncio
import logging
import os
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import our new modules
from config.environments import get_current_environment, get_environment_config, DataEnvironment
from data.factory import get_grant_source, get_impact_source, get_research_source, get_metrics_source
from data.quality.validator import validate_data_quality


async def test_environment_detection():
    """Test environment detection and configuration."""
    logger.info("🔍 Testing Environment Detection")
    
    # Test current environment
    current_env = get_current_environment()
    config = get_environment_config()
    
    logger.info(f"Current Environment: {current_env.value}")
    logger.info(f"Use Real Data: {config.use_real_data}")
    logger.info(f"API Mocking: {config.api_mocking}")
    logger.info(f"Quality Thresholds: {config.quality_thresholds}")
    
    # Test data sources
    logger.info(f"Grant Source: {config.grants_source}")
    logger.info(f"Impact Source: {config.impact_source}")
    logger.info(f"Research Source: {config.research_source}")
    logger.info(f"Metrics Source: {config.metrics_source}")
    
    return current_env, config


async def test_data_sources():
    """Test data source factory and data retrieval."""
    logger.info("🏭 Testing Data Source Factory")
    
    # Get data sources
    grant_source = get_grant_source()
    impact_source = get_impact_source()
    research_source = get_research_source()
    metrics_source = get_metrics_source()
    
    logger.info(f"Grant Source Type: {type(grant_source).__name__}")
    logger.info(f"Impact Source Type: {type(impact_source).__name__}")
    logger.info(f"Research Source Type: {type(research_source).__name__}")
    logger.info(f"Metrics Source Type: {type(metrics_source).__name__}")
    
    # Test data retrieval
    logger.info("📊 Testing Data Retrieval")
    
    grant_data = await grant_source.get_data()
    impact_data = await impact_source.get_data()
    research_data = await research_source.get_data()
    metrics_data = await metrics_source.get_data()
    
    logger.info(f"Grant Data Status: {grant_data.get('status')}")
    logger.info(f"Impact Data Status: {impact_data.get('status')}")
    logger.info(f"Research Data Status: {research_data.get('status')}")
    logger.info(f"Metrics Data Status: {metrics_data.get('status')}")
    
    return grant_data, impact_data, research_data, metrics_data


async def test_data_quality_validation(grant_data: Dict[str, Any], impact_data: Dict[str, Any], research_data: Dict[str, Any]):
    """Test data quality validation."""
    logger.info("✅ Testing Data Quality Validation")
    
    # Validate grant data
    grant_quality = validate_data_quality(grant_data, 'grants')
    logger.info(f"Grant Data Quality: {grant_quality.level.value} ({grant_quality.overall_score:.2%})")
    
    # Validate impact data
    impact_quality = validate_data_quality(impact_data, 'impact')
    logger.info(f"Impact Data Quality: {impact_quality.level.value} ({impact_quality.overall_score:.2%})")
    
    # Validate research data
    research_quality = validate_data_quality(research_data, 'research')
    logger.info(f"Research Data Quality: {research_quality.level.value} ({research_quality.overall_score:.2%})")
    
    # Log detailed quality reports
    logger.info("📋 Detailed Quality Reports:")
    
    for check in grant_quality.checks:
        status = "✅" if check.passed else "❌"
        logger.info(f"  {status} {check.name}: {check.details}")
    
    return grant_quality, impact_quality, research_quality


async def test_environment_switching():
    """Test switching between environments."""
    logger.info("🔄 Testing Environment Switching")
    
    # Test development environment
    os.environ['DATA_ENVIRONMENT'] = 'development'
    os.environ['USE_REAL_DATA'] = 'false'
    
    from config.environments import EnvironmentManager
    dev_manager = EnvironmentManager()
    dev_config = dev_manager.get_config()
    
    logger.info(f"Development Environment: {dev_manager.current_environment.value}")
    logger.info(f"Development - Use Real Data: {dev_config.use_real_data}")
    
    # Test production environment
    os.environ['DATA_ENVIRONMENT'] = 'production'
    os.environ['USE_REAL_DATA'] = 'true'
    
    prod_manager = EnvironmentManager()
    prod_config = prod_manager.get_config()
    
    logger.info(f"Production Environment: {prod_manager.current_environment.value}")
    logger.info(f"Production - Use Real Data: {prod_config.use_real_data}")
    
    # Reset to development
    os.environ['DATA_ENVIRONMENT'] = 'development'
    os.environ['USE_REAL_DATA'] = 'false'


async def test_data_source_validation():
    """Test data source connection validation."""
    logger.info("🔗 Testing Data Source Validation")
    
    # Get data sources
    grant_source = get_grant_source()
    impact_source = get_impact_source()
    research_source = get_research_source()
    metrics_source = get_metrics_source()
    
    # Test connections
    grant_valid = grant_source.validate_connection()
    impact_valid = impact_source.validate_connection()
    research_valid = research_source.validate_connection()
    metrics_valid = metrics_source.validate_connection()
    
    logger.info(f"Grant Source Connection: {'✅ Valid' if grant_valid else '❌ Invalid'}")
    logger.info(f"Impact Source Connection: {'✅ Valid' if impact_valid else '❌ Invalid'}")
    logger.info(f"Research Source Connection: {'✅ Valid' if research_valid else '❌ Invalid'}")
    logger.info(f"Metrics Source Connection: {'✅ Valid' if metrics_valid else '❌ Invalid'}")
    
    return grant_valid, impact_valid, research_valid, metrics_valid


async def generate_test_report():
    """Generate a comprehensive test report."""
    logger.info("📊 Generating Test Report")
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "tests": {}
    }
    
    # Test 1: Environment Detection
    try:
        current_env, config = await test_environment_detection()
        report["tests"]["environment_detection"] = {
            "status": "passed",
            "environment": current_env.value,
            "use_real_data": config.use_real_data
        }
    except Exception as e:
        report["tests"]["environment_detection"] = {
            "status": "failed",
            "error": str(e)
        }
    
    # Test 2: Data Sources
    try:
        grant_data, impact_data, research_data, metrics_data = await test_data_sources()
        report["tests"]["data_sources"] = {
            "status": "passed",
            "grant_status": grant_data.get('status'),
            "impact_status": impact_data.get('status'),
            "research_status": research_data.get('status'),
            "metrics_status": metrics_data.get('status')
        }
    except Exception as e:
        report["tests"]["data_sources"] = {
            "status": "failed",
            "error": str(e)
        }
    
    # Test 3: Quality Validation
    try:
        grant_quality, impact_quality, research_quality = await test_data_quality_validation(
            grant_data, impact_data, research_data
        )
        report["tests"]["quality_validation"] = {
            "status": "passed",
            "grant_quality": grant_quality.level.value,
            "impact_quality": impact_quality.level.value,
            "research_quality": research_quality.level.value
        }
    except Exception as e:
        report["tests"]["quality_validation"] = {
            "status": "failed",
            "error": str(e)
        }
    
    # Test 4: Environment Switching
    try:
        await test_environment_switching()
        report["tests"]["environment_switching"] = {
            "status": "passed"
        }
    except Exception as e:
        report["tests"]["environment_switching"] = {
            "status": "failed",
            "error": str(e)
        }
    
    # Test 5: Connection Validation
    try:
        grant_valid, impact_valid, research_valid, metrics_valid = await test_data_source_validation()
        report["tests"]["connection_validation"] = {
            "status": "passed",
            "all_connections_valid": all([grant_valid, impact_valid, research_valid, metrics_valid])
        }
    except Exception as e:
        report["tests"]["connection_validation"] = {
            "status": "failed",
            "error": str(e)
        }
    
    # Calculate overall status
    passed_tests = sum(1 for test in report["tests"].values() if test["status"] == "passed")
    total_tests = len(report["tests"])
    
    report["summary"] = {
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "failed_tests": total_tests - passed_tests,
        "success_rate": passed_tests / total_tests if total_tests > 0 else 0
    }
    
    return report


async def main():
    """Main test function."""
    logger.info("🚀 Starting Real vs Test Data Implementation Tests")
    logger.info("=" * 60)
    
    try:
        # Run all tests
        report = await generate_test_report()
        
        # Print summary
        logger.info("=" * 60)
        logger.info("📋 Test Summary")
        logger.info(f"Total Tests: {report['summary']['total_tests']}")
        logger.info(f"Passed: {report['summary']['passed_tests']}")
        logger.info(f"Failed: {report['summary']['failed_tests']}")
        logger.info(f"Success Rate: {report['summary']['success_rate']:.2%}")
        
        if report['summary']['success_rate'] >= 0.8:
            logger.info("🎉 Real vs Test Data Implementation: SUCCESS!")
        else:
            logger.warning("⚠️ Real vs Test Data Implementation: NEEDS ATTENTION")
        
        return report
        
    except Exception as e:
        logger.error(f"❌ Test execution failed: {e}")
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    # Import datetime for the report
    from datetime import datetime
    
    # Run the tests
    result = asyncio.run(main())
    
    # Print final result
    if isinstance(result, dict) and result.get("status") == "error":
        print(f"\n❌ Test failed: {result['message']}")
    else:
        print(f"\n✅ Tests completed successfully!")
        print(f"Success Rate: {result['summary']['success_rate']:.2%}") 