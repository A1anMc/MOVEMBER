#!/usr/bin/env python3
"""
Enhanced Data Pipeline for Advanced Analytics and Machine Learning
Collects, processes, and stores comprehensive data for ML model training.
"""

import asyncio
import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json
import sqlalchemy
from sqlalchemy import create_engine, text
import os
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class DataSource(Enum):
    """Data sources for ML training."""
    GRANT_APPLICATIONS = "grant_applications"
    RULE_EVALUATIONS = "rule_evaluations"
    STAKEHOLDER_FEEDBACK = "stakeholder_feedback"
    PERFORMANCE_METRICS = "performance_metrics"
    SDG_ALIGNMENT = "sdg_alignment"
    IMPACT_MEASUREMENTS = "impact_measurements"
    EXTERNAL_DATASETS = "external_datasets"

@dataclass
class MLDataPoint:
    """Structured data point for ML training."""
    grant_id: str
    timestamp: datetime
    features: Dict[str, Any]
    labels: Dict[str, Any]
    metadata: Dict[str, Any]
    source: DataSource

class EnhancedDataPipeline:
    """Enhanced data pipeline for ML model training."""

    def __init__(self, database_url: str = None):
        self.database_url = database_url or os.getenv('DATABASE_URL', 'sqlite:///ml_data.db')
        self.engine = create_engine(self.database_url)
        self.data_cache = {}
        self.feature_columns = self._define_feature_columns()
        self.label_columns = self._define_label_columns()

    def _define_feature_columns(self) -> Dict[str, List[str]]:
        """Define feature columns for different ML tasks."""
        return {
            "grant_evaluation": [
                "amount", "timeline_months", "category_encoded",
                "target_demographic_encoded", "location_encoded",
                "organisation_size", "contact_experience_level",
                "description_length", "has_budget_breakdown",
                "has_timeline_details", "has_stakeholder_plan",
                "has_impact_metrics", "has_sdg_alignment",
                "submission_month", "submission_day_of_week"
            ],
            "impact_prediction": [
                "grant_amount", "program_duration", "target_population_size",
                "geographic_coverage", "intervention_type",
                "stakeholder_engagement_level", "evidence_base_strength",
                "implementation_complexity", "resource_availability",
                "policy_environment", "community_readiness"
            ],
            "sdg_alignment": [
                "sdg_3_alignment", "sdg_4_alignment", "sdg_10_alignment",
                "sdg_11_alignment", "sdg_17_alignment",
                "mental_health_focus", "education_component",
                "equity_consideration", "community_involvement",
                "partnership_approach"
            ],
            "stakeholder_engagement": [
                "beneficiary_involvement", "healthcare_provider_engagement",
                "community_organization_partnership", "policymaker_consultation",
                "funder_communication", "researcher_collaboration",
                "feedback_mechanisms", "capacity_building_activities"
            ]
        }

    def _define_label_columns(self) -> Dict[str, List[str]]:
        """Define label columns for different ML tasks."""
        return {
            "grant_evaluation": [
                "overall_score", "approval_probability", "risk_level",
                "impact_potential", "sustainability_score"
            ],
            "impact_prediction": [
                "participant_outreach", "behavior_change_rate",
                "service_utilization_increase", "stigma_reduction",
                "policy_influence_level", "community_capacity_building"
            ],
            "sdg_alignment": [
                "sdg_3_contribution", "sdg_4_contribution", "sdg_10_contribution",
                "sdg_11_contribution", "sdg_17_contribution",
                "overall_sdg_alignment_score"
            ],
            "stakeholder_engagement": [
                "engagement_effectiveness", "partnership_success_rate",
                "feedback_quality", "capacity_building_impact",
                "sustainability_indicators"
            ]
        }

    async def collect_grant_data(self, grant_data: Dict[str, Any]) -> MLDataPoint:
        """Collect and structure grant data for ML training."""
        features = self._extract_grant_features(grant_data)
        labels = self._extract_grant_labels(grant_data)

        return MLDataPoint(
            grant_id=grant_data.get("grant_id", ""),
            timestamp=datetime.now(),
            features=features,
            labels=labels,
            metadata={
                "source": "grant_application",
                "category": grant_data.get("category", ""),
                "amount": grant_data.get("amount", 0),
                "location": grant_data.get("location", "")
            },
            source=DataSource.GRANT_APPLICATIONS
        )

    def _extract_grant_features(self, grant_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract features from grant data."""
        features = {}

        # Basic features
        features["amount"] = float(grant_data.get("amount", 0))
        features["timeline_months"] = int(grant_data.get("timeline_months", 0))

        # Categorical encoding
        features["category_encoded"] = self._encode_category(grant_data.get("category", ""))
        features["target_demographic_encoded"] = self._encode_demographic(grant_data.get("target_demographic", ""))
        features["location_encoded"] = self._encode_location(grant_data.get("location", ""))

        # Derived features
        features["organisation_size"] = self._estimate_organisation_size(grant_data.get("organisation", ""))
        features["contact_experience_level"] = self._estimate_contact_experience(grant_data.get("contact_person", ""))
        features["description_length"] = len(grant_data.get("description", ""))
        features["has_budget_breakdown"] = 1 if grant_data.get("budget") else 0
        features["has_timeline_details"] = 1 if grant_data.get("timeline_months") else 0
        features["has_stakeholder_plan"] = self._check_stakeholder_plan(grant_data)
        features["has_impact_metrics"] = self._check_impact_metrics(grant_data)
        features["has_sdg_alignment"] = self._check_sdg_alignment(grant_data)

        # Temporal features
        submission_date = datetime.strptime(grant_data.get("submission_date", "2024-01-01"), "%Y-%m-%d")
        features["submission_month"] = submission_date.month
        features["submission_day_of_week"] = submission_date.weekday()

        return features

    def _extract_grant_labels(self, grant_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract labels from grant data."""
        labels = {}

        # Calculate scores based on rules engine evaluation
        evaluation_results = grant_data.get("evaluation_results", [])

        # Overall score (normalized 0-1)
        labels["overall_score"] = grant_data.get("score", 0) / 10.0

        # Approval probability (based on score threshold)
        labels["approval_probability"] = 1.0 if grant_data.get("score", 0) >= 7.0 else 0.5 if grant_data.get("score", 0) >= 5.0 else 0.0

        # Risk level (0=low, 1=medium, 2=high)
        score = grant_data.get("score", 0)
        if score >= 7.0:
            labels["risk_level"] = 0  # Low risk
        elif score >= 5.0:
            labels["risk_level"] = 1  # Medium risk
        else:
            labels["risk_level"] = 2  # High risk

        # Impact potential (based on amount and category)
        amount = grant_data.get("amount", 0)
        category = grant_data.get("category", "")
        if category == "mental_health" and amount > 50000:
            labels["impact_potential"] = 1.0
        elif category == "mental_health" and amount > 25000:
            labels["impact_potential"] = 0.7
        else:
            labels["impact_potential"] = 0.4

        # Sustainability score (based on timeline and stakeholder engagement)
        timeline = grant_data.get("timeline_months", 0)
        if timeline >= 24:
            labels["sustainability_score"] = 0.9
        elif timeline >= 12:
            labels["sustainability_score"] = 0.7
        else:
            labels["sustainability_score"] = 0.5

        return labels

    def _encode_category(self, category: str) -> int:
        """Encode category as integer."""
        category_mapping = {
            "mental_health": 1,
            "physical_health": 2,
            "education": 3,
            "community": 4,
            "research": 5
        }
        return category_mapping.get(category.lower(), 0)

    def _encode_demographic(self, demographic: str) -> int:
        """Encode demographic as integer."""
        demographic_mapping = {
            "young_men": 1,
            "men": 2,
            "all": 3,
            "women": 4,
            "children": 5
        }
        return demographic_mapping.get(demographic.lower(), 0)

    def _encode_location(self, location: str) -> int:
        """Encode location as integer."""
        location_mapping = {
            "victoria": 1,
            "new_south_wales": 2,
            "queensland": 3,
            "western_australia": 4,
            "south_australia": 5,
            "tasmania": 6,
            "northern_territory": 7,
            "australian_capital_territory": 8
        }
        return location_mapping.get(location.lower().replace(" ", "_"), 0)

    def _estimate_organisation_size(self, organisation: str) -> int:
        """Estimate organisation size based on name patterns."""
        org_lower = organisation.lower()
        if any(word in org_lower for word in ["university", "hospital", "government", "department"]):
            return 3  # Large
        elif any(word in org_lower for word in ["foundation", "institute", "association"]):
            return 2  # Medium
        else:
            return 1  # Small

    def _estimate_contact_experience(self, contact: str) -> int:
        """Estimate contact experience level."""
        contact_lower = contact.lower()
        if "dr." in contact_lower or "professor" in contact_lower:
            return 3  # High experience
        elif "manager" in contact_lower or "director" in contact_lower:
            return 2  # Medium experience
        else:
            return 1  # Low experience

    def _check_stakeholder_plan(self, grant_data: Dict[str, Any]) -> int:
        """Check if grant has stakeholder engagement plan."""
        description = grant_data.get("description", "").lower()
        keywords = ["stakeholder", "community", "partnership", "engagement"]
        return 1 if any(keyword in description for keyword in keywords) else 0

    def _check_impact_metrics(self, grant_data: Dict[str, Any]) -> int:
        """Check if grant has impact metrics."""
        description = grant_data.get("description", "").lower()
        keywords = ["impact", "outcome", "measurement", "evaluation", "metrics"]
        return 1 if any(keyword in description for keyword in keywords) else 0

    def _check_sdg_alignment(self, grant_data: Dict[str, Any]) -> int:
        """Check if grant has SDG alignment."""
        description = grant_data.get("description", "").lower()
        keywords = ["sdg", "sustainable development", "goal", "target"]
        return 1 if any(keyword in description for keyword in keywords) else 0

    async def collect_rule_evaluation_data(self, evaluation_results: List[Dict[str, Any]]) -> MLDataPoint:
        """Collect rule evaluation data for ML training."""
        features = self._extract_rule_features(evaluation_results)
        labels = self._extract_rule_labels(evaluation_results)

        return MLDataPoint(
            grant_id="rule_evaluation",
            timestamp=datetime.now(),
            features=features,
            labels=labels,
            metadata={
                "source": "rule_evaluation",
                "total_rules": len(evaluation_results),
                "triggered_rules": len([r for r in evaluation_results if r.get("conditions_met", False)])
            },
            source=DataSource.RULE_EVALUATIONS
        )

    def _extract_rule_features(self, evaluation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract features from rule evaluation results."""
        features = {}

        # Rule execution statistics
        features["total_rules"] = len(evaluation_results)
        features["triggered_rules"] = len([r for r in evaluation_results if r.get("conditions_met", False)])
        features["success_rate"] = len([r for r in evaluation_results if r.get("success", False)]) / len(evaluation_results) if evaluation_results else 0

        # Rule category distribution
        rule_categories = {}
        for result in evaluation_results:
            rule_name = result.get("rule_name", "")
            category = self._categorize_rule(rule_name)
            rule_categories[category] = rule_categories.get(category, 0) + 1

        features["validation_rules"] = rule_categories.get("validation", 0)
        features["impact_rules"] = rule_categories.get("impact", 0)
        features["stakeholder_rules"] = rule_categories.get("stakeholder", 0)
        features["performance_rules"] = rule_categories.get("performance", 0)

        # Execution time statistics
        execution_times = [r.get("execution_time", 0) for r in evaluation_results]
        features["avg_execution_time"] = np.mean(execution_times) if execution_times else 0
        features["max_execution_time"] = np.max(execution_times) if execution_times else 0

        return features

    def _extract_rule_labels(self, evaluation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract labels from rule evaluation results."""
        labels = {}

        # Overall evaluation quality
        success_count = len([r for r in evaluation_results if r.get("success", False)])
        labels["evaluation_quality"] = success_count / len(evaluation_results) if evaluation_results else 0

        # Rule effectiveness
        triggered_rules = [r for r in evaluation_results if r.get("conditions_met", False)]
        labels["rule_effectiveness"] = len(triggered_rules) / len(evaluation_results) if evaluation_results else 0

        # System performance
        avg_time = np.mean([r.get("execution_time", 0) for r in evaluation_results]) if evaluation_results else 0
        labels["system_performance"] = 1.0 if avg_time < 0.1 else 0.5 if avg_time < 0.5 else 0.0

        return labels

    def _categorize_rule(self, rule_name: str) -> str:
        """Categorize rule based on name."""
        rule_lower = rule_name.lower()
        if any(word in rule_lower for word in ["validate", "check", "ensure"]):
            return "validation"
        elif any(word in rule_lower for word in ["impact", "outcome", "effect"]):
            return "impact"
        elif any(word in rule_lower for word in ["stakeholder", "engagement", "partnership"]):
            return "stakeholder"
        elif any(word in rule_lower for word in ["performance", "optimize", "efficiency"]):
            return "performance"
        else:
            return "other"

    async def store_ml_data(self, data_point: MLDataPoint) -> bool:
        """Store ML data point in database."""
        try:
            # Convert to DataFrame for easy storage
            df_data = {
                "grant_id": data_point.grant_id,
                "timestamp": data_point.timestamp,
                "source": data_point.source.value,
                **data_point.features,
                **data_point.labels,
                "metadata": json.dumps(data_point.metadata)
            }

            df = pd.DataFrame([df_data])

            # Store in database
            table_name = f"ml_data_{data_point.source.value}"
            df.to_sql(table_name, self.engine, if_exists='append', index=False)

            logger.info(f"Stored ML data point for {data_point.grant_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to store ML data: {e}")
            return False

    async def get_training_data(self, task: str, limit: int = 1000) -> pd.DataFrame:
        """Get training data for specific ML task."""
        try:
            # Get data from all relevant tables
            tables = ["ml_data_grant_applications", "ml_data_rule_evaluations"]
            all_data = []

            for table in tables:
                query = f"SELECT * FROM {table} LIMIT {limit}"
                df = pd.read_sql(query, self.engine)
                all_data.append(df)

            # Combine data
            combined_df = pd.concat(all_data, ignore_index=True)

            # Select relevant features and labels
            features = self.feature_columns.get(task, [])
            labels = self.label_columns.get(task, [])

            # Filter columns
            available_columns = combined_df.columns.tolist()
            selected_features = [col for col in features if col in available_columns]
            selected_labels = [col for col in labels if col in available_columns]

            return combined_df[selected_features + selected_labels]

        except Exception as e:
            logger.error(f"Failed to get training data: {e}")
            return pd.DataFrame()

async def main():
    """Test the enhanced data pipeline."""
    pipeline = EnhancedDataPipeline()

    # Test with sample grant data
    sample_grant = {
        "grant_id": "ML-TEST-001",
        "title": "Machine Learning Test Grant",
        "description": "Test grant for ML data collection with impact metrics and SDG alignment",
        "amount": 75000,
        "budget": 75000,
        "timeline_months": 18,
        "category": "mental_health",
        "target_demographic": "young_men",
        "location": "Victoria",
        "organisation": "ML Research Institute",
        "contact_person": "Dr. ML Expert",
        "email": "ml@test.org.au",
        "submission_date": "2024-08-08",
        "score": 7.5,
        "evaluation_results": [
            {"rule_name": "validate_impact_metrics", "success": True, "conditions_met": True, "execution_time": 0.02},
            {"rule_name": "check_sdg_alignment", "success": True, "conditions_met": True, "execution_time": 0.01}
        ]
    }

    # Collect and store data
    grant_data_point = await pipeline.collect_grant_data(sample_grant)
    await pipeline.store_ml_data(grant_data_point)

    rule_data_point = await pipeline.collect_rule_evaluation_data(sample_grant["evaluation_results"])
    await pipeline.store_ml_data(rule_data_point)

    print("✅ Enhanced data pipeline ready for ML training!")
    print(f"Features collected: {len(grant_data_point.features)}")
    print(f"Labels generated: {len(grant_data_point.labels)}")

if __name__ == "__main__":
    asyncio.run(main())
