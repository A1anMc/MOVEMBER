#!/usr/bin/env python3
"""
Real Data Validation System
Validates accuracy and quality of real Movember data.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import re

logger = logging.getLogger(__name__)

class ValidationLevel(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class ValidationStatus(Enum):
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    UNKNOWN = "unknown"

@dataclass
class ValidationResult:
    """Result of a data validation check."""
    metric_name: str
    status: ValidationStatus
    level: ValidationLevel
    message: str
    expected_value: Optional[Any] = None
    actual_value: Optional[Any] = None
    confidence: float = 0.0
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class RealDataValidator:
    """Validates real Movember data for accuracy and quality."""
    
    def __init__(self):
        # Known valid ranges for Movember metrics
        self.valid_ranges = {
            "total_funding": {
                "min": 50000000,  # $50M AUD minimum
                "max": 500000000,  # $500M AUD maximum
                "unit": "AUD",
                "level": ValidationLevel.CRITICAL
            },
            "people_reached": {
                "min": 1000000,  # 1M people minimum
                "max": 50000000,  # 50M people maximum
                "unit": "people",
                "level": ValidationLevel.CRITICAL
            },
            "countries": {
                "min": 10,  # 10 countries minimum
                "max": 100,  # 100 countries maximum
                "unit": "countries",
                "level": ValidationLevel.HIGH
            },
            "research_projects": {
                "min": 100,  # 100 projects minimum
                "max": 2000,  # 2000 projects maximum
                "unit": "projects",
                "level": ValidationLevel.HIGH
            },
            "volunteer_hours": {
                "min": 10000,  # 10K hours minimum
                "max": 1000000,  # 1M hours maximum
                "unit": "hours",
                "level": ValidationLevel.MEDIUM
            }
        }
        
        # Expected data patterns
        self.expected_patterns = {
            "currency": r"^AUD$",
            "people_count": r"^\d+$",
            "percentage": r"^\d+(?:\.\d+)?%$",
            "date": r"^\d{4}-\d{2}-\d{2}$"
        }
    
    async def validate_movember_data(self, data: Dict[str, Any]) -> List[ValidationResult]:
        """Validate Movember data comprehensively."""
        results = []
        
        try:
            logger.info("Starting comprehensive data validation...")
            
            # Validate data structure
            results.extend(self._validate_data_structure(data))
            
            # Validate individual metrics
            for metric_name, metric_data in data.items():
                if metric_name in self.valid_ranges:
                    results.append(self._validate_metric(metric_name, metric_data))
            
            # Validate data freshness
            results.append(self._validate_data_freshness(data))
            
            # Validate data source
            results.append(self._validate_data_source(data))
            
            # Validate confidence levels
            results.extend(self._validate_confidence_levels(data))
            
            logger.info(f"Validation complete: {len(results)} checks performed")
            return results
            
        except Exception as e:
            logger.error(f"Error during data validation: {e}")
            return [ValidationResult(
                metric_name="validation_system",
                status=ValidationStatus.FAILED,
                level=ValidationLevel.CRITICAL,
                message=f"Validation system error: {e}"
            )]
    
    def _validate_data_structure(self, data: Dict[str, Any]) -> List[ValidationResult]:
        """Validate the overall data structure."""
        results = []
        
        # Check for required fields
        required_fields = ["data_source", "timestamp", "confidence"]
        for field in required_fields:
            if field not in data:
                results.append(ValidationResult(
                    metric_name=f"required_field_{field}",
                    status=ValidationStatus.FAILED,
                    level=ValidationLevel.CRITICAL,
                    message=f"Missing required field: {field}"
                ))
        
        # Check for at least one metric
        metric_count = sum(1 for k, v in data.items() 
                          if isinstance(v, dict) and "value" in v)
        if metric_count == 0:
            results.append(ValidationResult(
                metric_name="metric_count",
                status=ValidationStatus.FAILED,
                level=ValidationLevel.CRITICAL,
                message="No metrics found in data"
            ))
        
        return results
    
    def _validate_metric(self, metric_name: str, metric_data: Dict[str, Any]) -> ValidationResult:
        """Validate a single metric."""
        try:
            if not isinstance(metric_data, dict):
                return ValidationResult(
                    metric_name=metric_name,
                    status=ValidationStatus.FAILED,
                    level=ValidationLevel.CRITICAL,
                    message="Metric data is not a dictionary"
                )
            
            # Check for required metric fields
            if "value" not in metric_data:
                return ValidationResult(
                    metric_name=metric_name,
                    status=ValidationStatus.FAILED,
                    level=ValidationLevel.CRITICAL,
                    message="Missing value field"
                )
            
            value = metric_data["value"]
            valid_range = self.valid_ranges[metric_name]
            
            # Validate value range
            if not isinstance(value, (int, float)):
                return ValidationResult(
                    metric_name=metric_name,
                    status=ValidationStatus.FAILED,
                    level=valid_range["level"],
                    message=f"Value must be numeric, got {type(value)}",
                    actual_value=value
                )
            
            if value < valid_range["min"] or value > valid_range["max"]:
                return ValidationResult(
                    metric_name=metric_name,
                    status=ValidationStatus.WARNING,
                    level=valid_range["level"],
                    message=f"Value {value} outside expected range [{valid_range['min']}, {valid_range['max']}]",
                    expected_value=f"[{valid_range['min']}, {valid_range['max']}]",
                    actual_value=value
                )
            
            # Validate unit if present
            if "unit" in metric_data:
                expected_unit = valid_range["unit"]
                actual_unit = metric_data["unit"]
                if actual_unit != expected_unit:
                    return ValidationResult(
                        metric_name=metric_name,
                        status=ValidationStatus.WARNING,
                        level=valid_range["level"],
                        message=f"Unit mismatch: expected {expected_unit}, got {actual_unit}",
                        expected_value=expected_unit,
                        actual_value=actual_unit
                    )
            
            return ValidationResult(
                metric_name=metric_name,
                status=ValidationStatus.PASSED,
                level=valid_range["level"],
                message="Metric validation passed",
                actual_value=value,
                confidence=metric_data.get("confidence", 0.0)
            )
            
        except Exception as e:
            return ValidationResult(
                metric_name=metric_name,
                status=ValidationStatus.FAILED,
                level=ValidationLevel.CRITICAL,
                message=f"Validation error: {e}"
            )
    
    def _validate_data_freshness(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate that data is recent."""
        try:
            timestamp_str = data.get("timestamp")
            if not timestamp_str:
                return ValidationResult(
                    metric_name="data_freshness",
                    status=ValidationStatus.FAILED,
                    level=ValidationLevel.HIGH,
                    message="Missing timestamp"
                )
            
            # Parse timestamp
            if isinstance(timestamp_str, str):
                timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            else:
                timestamp = timestamp_str
            
            # Check if data is less than 24 hours old
            age = datetime.now(timestamp.tzinfo) - timestamp
            max_age = timedelta(hours=24)
            
            if age > max_age:
                return ValidationResult(
                    metric_name="data_freshness",
                    status=ValidationStatus.WARNING,
                    level=ValidationLevel.HIGH,
                    message=f"Data is {age.total_seconds() / 3600:.1f} hours old",
                    actual_value=f"{age.total_seconds() / 3600:.1f} hours"
                )
            
            return ValidationResult(
                metric_name="data_freshness",
                status=ValidationStatus.PASSED,
                level=ValidationLevel.HIGH,
                message="Data is fresh",
                actual_value=f"{age.total_seconds() / 3600:.1f} hours"
            )
            
        except Exception as e:
            return ValidationResult(
                metric_name="data_freshness",
                status=ValidationStatus.FAILED,
                level=ValidationLevel.HIGH,
                message=f"Timestamp validation error: {e}"
            )
    
    def _validate_data_source(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate the data source."""
        source = data.get("data_source", "unknown")
        
        # Preferred sources in order of reliability
        preferred_sources = [
            "movember_annual_reports",
            "movember_api",
            "official_website",
            "government_data"
        ]
        
        if source in preferred_sources:
            return ValidationResult(
                metric_name="data_source",
                status=ValidationStatus.PASSED,
                level=ValidationLevel.HIGH,
                message=f"Data source is reliable: {source}",
                actual_value=source
            )
        elif source == "fallback":
            return ValidationResult(
                metric_name="data_source",
                status=ValidationStatus.WARNING,
                level=ValidationLevel.MEDIUM,
                message="Using fallback data - real data unavailable",
                actual_value=source
            )
        else:
            return ValidationResult(
                metric_name="data_source",
                status=ValidationStatus.WARNING,
                level=ValidationLevel.MEDIUM,
                message=f"Unknown data source: {source}",
                actual_value=source
            )
    
    def _validate_confidence_levels(self, data: Dict[str, Any]) -> List[ValidationResult]:
        """Validate confidence levels across all metrics."""
        results = []
        
        # Check overall confidence
        overall_confidence = data.get("confidence", 0.0)
        if overall_confidence < 0.5:
            results.append(ValidationResult(
                metric_name="overall_confidence",
                status=ValidationStatus.WARNING,
                level=ValidationLevel.HIGH,
                message=f"Low overall confidence: {overall_confidence}",
                actual_value=overall_confidence
            ))
        
        # Check individual metric confidence levels
        for metric_name, metric_data in data.items():
            if isinstance(metric_data, dict) and "confidence" in metric_data:
                confidence = metric_data["confidence"]
                if confidence < 0.7:
                    results.append(ValidationResult(
                        metric_name=f"{metric_name}_confidence",
                        status=ValidationStatus.WARNING,
                        level=ValidationLevel.MEDIUM,
                        message=f"Low confidence for {metric_name}: {confidence}",
                        actual_value=confidence
                    ))
        
        return results
    
    def get_validation_summary(self, results: List[ValidationResult]) -> Dict[str, Any]:
        """Generate a summary of validation results."""
        summary = {
            "total_checks": len(results),
            "passed": sum(1 for r in results if r.status == ValidationStatus.PASSED),
            "failed": sum(1 for r in results if r.status == ValidationStatus.FAILED),
            "warnings": sum(1 for r in results if r.status == ValidationStatus.WARNING),
            "critical_issues": sum(1 for r in results if r.level == ValidationLevel.CRITICAL and r.status == ValidationStatus.FAILED),
            "overall_status": "passed" if not any(r.status == ValidationStatus.FAILED for r in results) else "failed",
            "timestamp": datetime.now().isoformat()
        }
        
        # Group by level
        for level in ValidationLevel:
            summary[f"{level.value}_checks"] = sum(1 for r in results if r.level == level)
        
        return summary

# Convenience function for easy integration
async def validate_movember_data(data: Dict[str, Any]) -> Tuple[List[ValidationResult], Dict[str, Any]]:
    """Validate Movember data and return results with summary."""
    validator = RealDataValidator()
    results = await validator.validate_movember_data(data)
    summary = validator.get_validation_summary(results)
    return results, summary

if __name__ == "__main__":
    # Test the validator
    async def test():
        test_data = {
            "total_funding": {
                "value": 125000000,
                "unit": "AUD",
                "confidence": 0.85
            },
            "people_reached": {
                "value": 8500000,
                "unit": "people",
                "confidence": 0.80
            },
            "data_source": "movember_annual_reports",
            "timestamp": datetime.now().isoformat(),
            "confidence": 0.85
        }
        
        results, summary = await validate_movember_data(test_data)
        print("Validation Results:")
        for result in results:
            print(f"  {result.metric_name}: {result.status.value} - {result.message}")
        
        print("\nValidation Summary:")
        print(json.dumps(summary, indent=2, default=str))
    
    asyncio.run(test())
