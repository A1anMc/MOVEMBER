#!/usr/bin/env python3
"""
Data Quality Validation Framework
Validates data quality based on environment and thresholds.
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from config.environments import get_current_environment, get_environment_config, DataEnvironment

logger = logging.getLogger(__name__)


class QualityLevel(Enum):
    """Quality assessment levels."""
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    POOR = "poor"
    FAILED = "failed"


@dataclass
class QualityCheck:
    """Individual quality check result."""
    name: str
    passed: bool
    score: float
    details: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class QualityReport:
    """Comprehensive quality report."""
    overall_score: float
    level: QualityLevel
    checks: List[QualityCheck] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    environment: str = ""
    data_type: str = ""
    
    def add_check(self, check: QualityCheck):
        """Add a quality check to the report."""
        self.checks.append(check)
        self._update_overall_score()
    
    def _update_overall_score(self):
        """Update overall score based on individual checks."""
        if self.checks:
            self.overall_score = sum(check.score for check in self.checks) / len(self.checks)
            self.level = self._determine_level(self.overall_score)
    
    def _determine_level(self, score: float) -> QualityLevel:
        """Determine quality level based on score."""
        if score >= 0.95:
            return QualityLevel.EXCELLENT
        elif score >= 0.85:
            return QualityLevel.GOOD
        elif score >= 0.75:
            return QualityLevel.ACCEPTABLE
        elif score >= 0.60:
            return QualityLevel.POOR
        else:
            return QualityLevel.FAILED
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary."""
        return {
            "overall_score": self.overall_score,
            "level": self.level.value,
            "checks": [
                {
                    "name": check.name,
                    "passed": check.passed,
                    "score": check.score,
                    "details": check.details,
                    "timestamp": check.timestamp.isoformat()
                }
                for check in self.checks
            ],
            "timestamp": self.timestamp.isoformat(),
            "environment": self.environment,
            "data_type": self.data_type
        }


class DataQualityValidator:
    """Validates data quality based on environment and thresholds."""
    
    def __init__(self):
        self.environment = get_current_environment()
        self.config = get_environment_config()
        self.thresholds = self.config.quality_thresholds
        logger.info(f"Initialized validator for {self.environment.value} environment")
    
    def validate_grant_data(self, data: Dict[str, Any]) -> QualityReport:
        """Validate grant data quality."""
        report = QualityReport(
            overall_score=0.0,
            level=QualityLevel.FAILED,
            environment=self.environment.value,
            data_type="grants"
        )
        
        # Different validation for real vs test data
        if self.environment == DataEnvironment.PRODUCTION:
            self._validate_real_grant_data(data, report)
        else:
            self._validate_test_grant_data(data, report)
        
        return report
    
    def validate_impact_data(self, data: Dict[str, Any]) -> QualityReport:
        """Validate impact data quality."""
        report = QualityReport(
            overall_score=0.0,
            level=QualityLevel.FAILED,
            environment=self.environment.value,
            data_type="impact"
        )
        
        if self.environment == DataEnvironment.PRODUCTION:
            self._validate_real_impact_data(data, report)
        else:
            self._validate_test_impact_data(data, report)
        
        return report
    
    def validate_research_data(self, data: Dict[str, Any]) -> QualityReport:
        """Validate research data quality."""
        report = QualityReport(
            overall_score=0.0,
            level=QualityLevel.FAILED,
            environment=self.environment.value,
            data_type="research"
        )
        
        if self.environment == DataEnvironment.PRODUCTION:
            self._validate_real_research_data(data, report)
        else:
            self._validate_test_research_data(data, report)
        
        return report
    
    def _validate_real_grant_data(self, data: Dict[str, Any], report: QualityReport):
        """Validate real grant data with strict requirements."""
        
        # Check API authenticity
        check = self._check_api_authenticity(data)
        report.add_check(check)
        
        # Check data freshness
        check = self._check_data_freshness(data)
        report.add_check(check)
        
        # Check completeness
        check = self._check_completeness(data, ['grant_id', 'title', 'budget', 'deadline'])
        report.add_check(check)
        
        # Check data format
        check = self._check_data_format(data)
        report.add_check(check)
        
        # Check currency consistency
        check = self._check_currency_consistency(data)
        report.add_check(check)
    
    def _validate_test_grant_data(self, data: Dict[str, Any], report: QualityReport):
        """Validate test grant data with relaxed requirements."""
        
        # Check sample consistency
        check = self._check_sample_consistency(data)
        report.add_check(check)
        
        # Check test coverage
        check = self._check_test_coverage(data)
        report.add_check(check)
        
        # Check basic format
        check = self._check_basic_format(data)
        report.add_check(check)
    
    def _validate_real_impact_data(self, data: Dict[str, Any], report: QualityReport):
        """Validate real impact data."""
        
        # Check database authenticity
        check = self._check_database_authenticity(data)
        report.add_check(check)
        
        # Check impact metrics
        check = self._check_impact_metrics(data)
        report.add_check(check)
        
        # Check data consistency
        check = self._check_data_consistency(data)
        report.add_check(check)
    
    def _validate_test_impact_data(self, data: Dict[str, Any], report: QualityReport):
        """Validate test impact data."""
        
        # Check test data structure
        check = self._check_test_structure(data)
        report.add_check(check)
        
        # Check mock data quality
        check = self._check_mock_data_quality(data)
        report.add_check(check)
    
    def _validate_real_research_data(self, data: Dict[str, Any], report: QualityReport):
        """Validate real research data."""
        
        # Check API authenticity
        check = self._check_api_authenticity(data)
        report.add_check(check)
        
        # Check research metadata
        check = self._check_research_metadata(data)
        report.add_check(check)
    
    def _validate_test_research_data(self, data: Dict[str, Any], report: QualityReport):
        """Validate test research data."""
        
        # Check mock research structure
        check = self._check_mock_research_structure(data)
        report.add_check(check)
    
    def _check_api_authenticity(self, data: Dict[str, Any]) -> QualityCheck:
        """Check if data comes from authentic API source."""
        source = data.get('source', '')
        is_authentic = source in ['real_api', 'movember_database', 'pubmed_api', 'production_dashboard']
        
        return QualityCheck(
            name="api_authenticity",
            passed=is_authentic,
            score=1.0 if is_authentic else 0.0,
            details=f"Data source: {source} - {'Authentic' if is_authentic else 'Not authentic'}"
        )
    
    def _check_data_freshness(self, data: Dict[str, Any]) -> QualityCheck:
        """Check if data is fresh (within acceptable age)."""
        timestamp_str = data.get('timestamp', '')
        if not timestamp_str:
            return QualityCheck(
                name="data_freshness",
                passed=False,
                score=0.0,
                details="No timestamp found"
            )
        
        try:
            data_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            age_hours = (datetime.now() - data_time).total_seconds() / 3600
            
            # Accept data up to 24 hours old
            is_fresh = age_hours <= 24
            score = max(0.0, 1.0 - (age_hours / 24))
            
            return QualityCheck(
                name="data_freshness",
                passed=is_fresh,
                score=score,
                details=f"Data age: {age_hours:.1f} hours - {'Fresh' if is_fresh else 'Stale'}"
            )
        except Exception as e:
            return QualityCheck(
                name="data_freshness",
                passed=False,
                score=0.0,
                details=f"Error parsing timestamp: {e}"
            )
    
    def _check_completeness(self, data: Dict[str, Any], required_fields: List[str]) -> QualityCheck:
        """Check data completeness."""
        if not isinstance(data, dict):
            return QualityCheck(
                name="completeness",
                passed=False,
                score=0.0,
                details="Data is not a dictionary"
            )
        
        missing_fields = [field for field in required_fields if field not in data]
        completeness_ratio = 1.0 - (len(missing_fields) / len(required_fields))
        
        return QualityCheck(
            name="completeness",
            passed=completeness_ratio >= self.thresholds.completeness,
            score=completeness_ratio,
            details=f"Missing fields: {missing_fields} - Completeness: {completeness_ratio:.2%}"
        )
    
    def _check_data_format(self, data: Dict[str, Any]) -> QualityCheck:
        """Check data format consistency."""
        # Check if data has expected structure
        has_status = 'status' in data
        has_timestamp = 'timestamp' in data
        has_environment = 'environment' in data
        
        format_score = sum([has_status, has_timestamp, has_environment]) / 3
        
        return QualityCheck(
            name="data_format",
            passed=format_score >= 0.8,
            score=format_score,
            details=f"Format check: status={has_status}, timestamp={has_timestamp}, environment={has_environment}"
        )
    
    def _check_currency_consistency(self, data: Dict[str, Any]) -> QualityCheck:
        """Check currency consistency (should be AUD)."""
        currency = data.get('currency', '')
        is_aud = currency.upper() == 'AUD'
        
        return QualityCheck(
            name="currency_consistency",
            passed=is_aud,
            score=1.0 if is_aud else 0.0,
            details=f"Currency: {currency} - {'AUD (correct)' if is_aud else 'Not AUD'}"
        )
    
    def _check_sample_consistency(self, data: Dict[str, Any]) -> QualityCheck:
        """Check sample data consistency."""
        source = data.get('source', '')
        is_sample = source in ['sample_data', 'test_data', 'mock_data']
        
        return QualityCheck(
            name="sample_consistency",
            passed=is_sample,
            score=1.0 if is_sample else 0.0,
            details=f"Data source: {source} - {'Sample data' if is_sample else 'Not sample data'}"
        )
    
    def _check_test_coverage(self, data: Dict[str, Any]) -> QualityCheck:
        """Check test data coverage."""
        # Check if test data covers various scenarios
        data_keys = list(data.keys()) if isinstance(data, dict) else []
        coverage_score = min(1.0, len(data_keys) / 5)  # Expect at least 5 fields
        
        return QualityCheck(
            name="test_coverage",
            passed=coverage_score >= 0.6,
            score=coverage_score,
            details=f"Test coverage: {len(data_keys)} fields - Score: {coverage_score:.2%}"
        )
    
    def _check_basic_format(self, data: Dict[str, Any]) -> QualityCheck:
        """Check basic data format."""
        is_dict = isinstance(data, dict)
        has_data = 'data' in data or len(data) > 0
        
        format_score = 1.0 if (is_dict and has_data) else 0.0
        
        return QualityCheck(
            name="basic_format",
            passed=format_score > 0,
            score=format_score,
            details=f"Basic format: dict={is_dict}, has_data={has_data}"
        )
    
    def _check_database_authenticity(self, data: Dict[str, Any]) -> QualityCheck:
        """Check database authenticity."""
        source = data.get('source', '')
        is_database = source in ['movember_database', 'production_dashboard']
        
        return QualityCheck(
            name="database_authenticity",
            passed=is_database,
            score=1.0 if is_database else 0.0,
            details=f"Database source: {source} - {'Authentic' if is_database else 'Not authentic'}"
        )
    
    def _check_impact_metrics(self, data: Dict[str, Any]) -> QualityCheck:
        """Check impact metrics quality."""
        impact_data = data.get('data', {})
        required_metrics = ['men_reached', 'countries_reached', 'awareness_increase']
        
        missing_metrics = [metric for metric in required_metrics if metric not in impact_data]
        completeness = 1.0 - (len(missing_metrics) / len(required_metrics))
        
        return QualityCheck(
            name="impact_metrics",
            passed=completeness >= 0.8,
            score=completeness,
            details=f"Missing metrics: {missing_metrics} - Completeness: {completeness:.2%}"
        )
    
    def _check_data_consistency(self, data: Dict[str, Any]) -> QualityCheck:
        """Check data consistency."""
        # Check if numeric values are reasonable
        impact_data = data.get('data', {})
        men_reached = impact_data.get('men_reached', 0)
        
        is_consistent = men_reached > 0 and men_reached <= 10000000  # Reasonable range
        
        return QualityCheck(
            name="data_consistency",
            passed=is_consistent,
            score=1.0 if is_consistent else 0.0,
            details=f"Men reached: {men_reached} - {'Consistent' if is_consistent else 'Inconsistent'}"
        )
    
    def _check_test_structure(self, data: Dict[str, Any]) -> QualityCheck:
        """Check test data structure."""
        has_required = all(key in data for key in ['status', 'source', 'data', 'timestamp'])
        
        return QualityCheck(
            name="test_structure",
            passed=has_required,
            score=1.0 if has_required else 0.0,
            details=f"Test structure: {'Complete' if has_required else 'Incomplete'}"
        )
    
    def _check_mock_data_quality(self, data: Dict[str, Any]) -> QualityCheck:
        """Check mock data quality."""
        source = data.get('source', '')
        is_mock = source in ['test_data', 'mock_data']
        
        return QualityCheck(
            name="mock_data_quality",
            passed=is_mock,
            score=1.0 if is_mock else 0.0,
            details=f"Mock data source: {source} - {'Valid' if is_mock else 'Invalid'}"
        )
    
    def _check_research_metadata(self, data: Dict[str, Any]) -> QualityCheck:
        """Check research metadata."""
        research_data = data.get('data', [])
        if not isinstance(research_data, list):
            return QualityCheck(
                name="research_metadata",
                passed=False,
                score=0.0,
                details="Research data is not a list"
            )
        
        has_metadata = len(research_data) > 0
        return QualityCheck(
            name="research_metadata",
            passed=has_metadata,
            score=1.0 if has_metadata else 0.0,
            details=f"Research entries: {len(research_data)} - {'Has metadata' if has_metadata else 'No metadata'}"
        )
    
    def _check_mock_research_structure(self, data: Dict[str, Any]) -> QualityCheck:
        """Check mock research structure."""
        source = data.get('source', '')
        is_mock = source == 'mock_data'
        
        return QualityCheck(
            name="mock_research_structure",
            passed=is_mock,
            score=1.0 if is_mock else 0.0,
            details=f"Mock research source: {source} - {'Valid' if is_mock else 'Invalid'}"
        )


# Global validator instance
data_quality_validator = DataQualityValidator()


def validate_data_quality(data: Dict[str, Any], data_type: str) -> QualityReport:
    """Validate data quality for given data type."""
    if data_type == 'grants':
        return data_quality_validator.validate_grant_data(data)
    elif data_type == 'impact':
        return data_quality_validator.validate_impact_data(data)
    elif data_type == 'research':
        return data_quality_validator.validate_research_data(data)
    else:
        logger.warning(f"Unknown data type: {data_type}")
        return QualityReport(
            overall_score=0.0,
            level=QualityLevel.FAILED,
            environment=get_current_environment().value,
            data_type=data_type
        ) 