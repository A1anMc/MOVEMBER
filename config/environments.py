#!/usr/bin/env python3
"""
Environment Configuration System
Manages data sources and configuration based on environment.
"""

import os
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class DataEnvironment(Enum):
    """Data environment types."""
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


@dataclass
class QualityThresholds:
    """Quality thresholds for different environments."""
    completeness: float
    accuracy: float
    consistency: float
    timeliness: float


@dataclass
class DataSourceConfig:
    """Configuration for data sources in different environments."""
    grants_source: str
    impact_source: str
    research_source: str
    metrics_source: str
    api_mocking: bool
    use_real_data: bool
    quality_thresholds: QualityThresholds


class EnvironmentManager:
    """Manages environment detection and configuration."""
    
    def __init__(self):
        self.current_environment = self._detect_environment()
        self.config = self._get_environment_config()
        logger.info(f"Environment detected: {self.current_environment.value}")
    
    def _detect_environment(self) -> DataEnvironment:
        """Detect current data environment."""
        # Check environment variables first
        env_var = os.getenv('DATA_ENVIRONMENT', '').lower()
        use_real_data = os.getenv('USE_REAL_DATA', 'false').lower() == 'true'
        
        if use_real_data:
            return DataEnvironment.PRODUCTION
        elif env_var in ['production', 'prod']:
            return DataEnvironment.PRODUCTION
        elif env_var in ['staging', 'stage']:
            return DataEnvironment.STAGING
        elif env_var in ['testing', 'test']:
            return DataEnvironment.TESTING
        else:
            return DataEnvironment.DEVELOPMENT
    
    def _get_environment_config(self) -> DataSourceConfig:
        """Get configuration for current environment."""
        env = self.current_environment
        
        if env == DataEnvironment.PRODUCTION:
            return DataSourceConfig(
                grants_source="real_api_endpoints",
                impact_source="movember_database",
                research_source="pubmed_api",
                metrics_source="production_dashboard",
                api_mocking=False,
                use_real_data=True,
                quality_thresholds=QualityThresholds(
                    completeness=0.95,
                    accuracy=0.90,
                    consistency=0.85,
                    timeliness=0.80
                )
            )
        elif env == DataEnvironment.STAGING:
            return DataSourceConfig(
                grants_source="staging_api_endpoints",
                impact_source="staging_database",
                research_source="staging_pubmed",
                metrics_source="staging_dashboard",
                api_mocking=False,
                use_real_data=True,
                quality_thresholds=QualityThresholds(
                    completeness=0.90,
                    accuracy=0.85,
                    consistency=0.80,
                    timeliness=0.75
                )
            )
        elif env == DataEnvironment.TESTING:
            return DataSourceConfig(
                grants_source="test_api_endpoints",
                impact_source="test_database",
                research_source="mock_pubmed",
                metrics_source="test_dashboard",
                api_mocking=True,
                use_real_data=False,
                quality_thresholds=QualityThresholds(
                    completeness=0.85,
                    accuracy=0.80,
                    consistency=0.75,
                    timeliness=0.70
                )
            )
        else:  # DEVELOPMENT
            return DataSourceConfig(
                grants_source="sample_data/grants_2024.csv",
                impact_source="sample_data/impact_metrics_2024.csv",
                research_source="mock_research_data",
                metrics_source="test_metrics",
                api_mocking=True,
                use_real_data=False,
                quality_thresholds=QualityThresholds(
                    completeness=0.80,
                    accuracy=0.75,
                    consistency=0.70,
                    timeliness=0.65
                )
            )
    
    def get_config(self) -> DataSourceConfig:
        """Get current environment configuration."""
        return self.config
    
    def is_production(self) -> bool:
        """Check if current environment is production."""
        return self.current_environment == DataEnvironment.PRODUCTION
    
    def is_real_data_enabled(self) -> bool:
        """Check if real data is enabled for current environment."""
        return self.config.use_real_data
    
    def get_quality_thresholds(self) -> QualityThresholds:
        """Get quality thresholds for current environment."""
        return self.config.quality_thresholds
    
    def get_data_source(self, source_type: str) -> str:
        """Get data source for specific type."""
        source_map = {
            'grants': self.config.grants_source,
            'impact': self.config.impact_source,
            'research': self.config.research_source,
            'metrics': self.config.metrics_source
        }
        return source_map.get(source_type, 'unknown')


# Global environment manager instance
environment_manager = EnvironmentManager()


def get_current_environment() -> DataEnvironment:
    """Get current environment."""
    return environment_manager.current_environment


def get_environment_config() -> DataSourceConfig:
    """Get current environment configuration."""
    return environment_manager.get_config()


def is_production_environment() -> bool:
    """Check if current environment is production."""
    return environment_manager.is_production()


def is_real_data_enabled() -> bool:
    """Check if real data is enabled."""
    return environment_manager.is_real_data_enabled() 