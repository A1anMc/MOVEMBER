#!/usr/bin/env python3
"""
Advanced ML Engine for Movember AI Rules System - Phase 2
Machine learning integration with predictive analytics and intelligent rule optimization
"""

import asyncio
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
import logging
import json
import sqlite3
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
import joblib
import os
from collections import defaultdict

logger = logging.getLogger(__name__)

@dataclass
class PredictionResult:
    """Prediction result with confidence and metadata."""
    prediction: float
    confidence: float
    model_name: str
    features_used: List[str]
    timestamp: datetime
    context: Dict[str, Any] = None

@dataclass
class RuleOptimization:
    """Rule optimization recommendation."""
    rule_name: str
    current_performance: float
    suggested_improvement: float
    optimization_type: str
    confidence: float
    reasoning: str

class AdvancedMLEngine:
    """Advanced ML engine for predictive analytics and rule optimization."""

    def __init__(self, models_dir: str = "ml_models"):
        self.models_dir = models_dir
        self.models = {}
        self.scalers = {}
        self.feature_importance = {}
        self.performance_history = defaultdict(list)

        # Ensure models directory exists
        os.makedirs(models_dir, exist_ok=True)

        # Initialize models
        self._initialize_models()

        logger.info("Advanced ML Engine initialized")

    def _initialize_models(self):
        """Initialize ML models for different prediction tasks."""
        # Grant success prediction model
        self.models['grant_success'] = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )

        # Impact outcome prediction model
        self.models['impact_outcome'] = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )

        # Rule performance prediction model
        self.models['rule_performance'] = LinearRegression()

        # Risk assessment model
        self.models['risk_assessment'] = LogisticRegression(random_state=42)

        # Initialize scalers
        for model_name in self.models.keys():
            self.scalers[model_name] = StandardScaler()

    async def predict_grant_success(self, grant_data: Dict[str, Any]) -> PredictionResult:
        """Predict grant application success probability."""
        try:
            # Extract features
            features = self._extract_grant_features(grant_data)

            # Get or train model
            model = await self._get_or_train_model('grant_success', features)

            # Make prediction
            prediction = model.predict_proba([features])[0][1]  # Success probability
            confidence = self._calculate_confidence(model, features)

            return PredictionResult(
                prediction=prediction,
                confidence=confidence,
                model_name="grant_success",
                features_used=list(self._get_grant_feature_names()),
                timestamp=datetime.now(),
                context=grant_data
            )

        except Exception as e:
            logger.error(f"Error predicting grant success: {str(e)}")
            raise

    async def predict_impact_outcome(self, project_data: Dict[str, Any]) -> PredictionResult:
        """Predict project impact outcome score."""
        try:
            # Extract features
            features = self._extract_impact_features(project_data)

            # Get or train model
            model = await self._get_or_train_model('impact_outcome', features)

            # Make prediction
            prediction = model.predict([features])[0]
            confidence = self._calculate_confidence(model, features)

            return PredictionResult(
                prediction=prediction,
                confidence=confidence,
                model_name="impact_outcome",
                features_used=list(self._get_impact_feature_names()),
                timestamp=datetime.now(),
                context=project_data
            )

        except Exception as e:
            logger.error(f"Error predicting impact outcome: {str(e)}")
            raise

    async def optimize_rules(self, rule_performance_data: List[Dict[str, Any]]) -> List[RuleOptimization]:
        """Optimize rules based on performance data."""
        try:
            optimizations = []

            for rule_data in rule_performance_data:
                # Extract rule features
                features = self._extract_rule_features(rule_data)

                # Get or train model
                model = await self._get_or_train_model('rule_performance', features)

                # Predict optimal performance
                predicted_performance = model.predict([features])[0]
                current_performance = rule_data.get('current_performance', 0.5)

                # Calculate improvement potential
                improvement = predicted_performance - current_performance
                confidence = self._calculate_confidence(model, features)

                if improvement > 0.1:  # Significant improvement potential
                    optimization = RuleOptimization(
                        rule_name=rule_data.get('rule_name', 'unknown'),
                        current_performance=current_performance,
                        suggested_improvement=improvement,
                        optimization_type=self._determine_optimization_type(rule_data),
                        confidence=confidence,
                        reasoning=self._generate_optimization_reasoning(rule_data, improvement)
                    )
                    optimizations.append(optimization)

            return optimizations

        except Exception as e:
            logger.error(f"Error optimizing rules: {str(e)}")
            raise

    async def assess_risk(self, project_data: Dict[str, Any]) -> PredictionResult:
        """Assess project risk level."""
        try:
            # Extract features
            features = self._extract_risk_features(project_data)

            # Get or train model
            model = await self._get_or_train_model('risk_assessment', features)

            # Make prediction
            risk_probability = model.predict_proba([features])[0][1]  # Risk probability
            confidence = self._calculate_confidence(model, features)

            return PredictionResult(
                prediction=risk_probability,
                confidence=confidence,
                model_name="risk_assessment",
                features_used=list(self._get_risk_feature_names()),
                timestamp=datetime.now(),
                context=project_data
            )

        except Exception as e:
            logger.error(f"Error assessing risk: {str(e)}")
            raise

    def _extract_grant_features(self, grant_data: Dict[str, Any]) -> List[float]:
        """Extract features for grant success prediction."""
        return [
            grant_data.get('budget', 0) / 100000,  # Normalized budget
            grant_data.get('timeline_months', 12) / 24,  # Normalized timeline
            len(grant_data.get('team_members', [])),
            len(grant_data.get('partnerships', [])),
            grant_data.get('experience_years', 0) / 20,  # Normalized experience
            grant_data.get('previous_success_rate', 0.5),
            len(grant_data.get('sdg_alignment', [])),
            grant_data.get('innovation_score', 0.5),
            grant_data.get('community_impact', 0.5),
            grant_data.get('sustainability_score', 0.5)
        ]

    def _extract_impact_features(self, project_data: Dict[str, Any]) -> List[float]:
        """Extract features for impact outcome prediction."""
        return [
            project_data.get('funding_amount', 0) / 1000000,  # Normalized funding
            project_data.get('duration_months', 12) / 36,  # Normalized duration
            project_data.get('participant_count', 0) / 10000,  # Normalized participants
            project_data.get('geographic_reach', 0) / 100,  # Normalized reach
            project_data.get('stakeholder_engagement', 0.5),
            project_data.get('methodology_quality', 0.5),
            project_data.get('baseline_data_quality', 0.5),
            project_data.get('evaluation_plan_quality', 0.5),
            project_data.get('partnership_strength', 0.5),
            project_data.get('innovation_level', 0.5)
        ]

    def _extract_rule_features(self, rule_data: Dict[str, Any]) -> List[float]:
        """Extract features for rule performance prediction."""
        return [
            rule_data.get('execution_count', 0) / 1000,  # Normalized execution count
            rule_data.get('success_rate', 0.5),
            rule_data.get('average_execution_time', 100) / 1000,  # Normalized time
            rule_data.get('complexity_score', 0.5),
            rule_data.get('dependency_count', 0) / 10,  # Normalized dependencies
            rule_data.get('last_updated_days', 30) / 365,  # Normalized age
            rule_data.get('error_rate', 0.0),
            rule_data.get('cache_hit_rate', 0.5),
            rule_data.get('priority_score', 0.5),
            rule_data.get('context_specificity', 0.5)
        ]

    def _extract_risk_features(self, project_data: Dict[str, Any]) -> List[float]:
        """Extract features for risk assessment."""
        return [
            project_data.get('budget_volatility', 0.0),
            project_data.get('timeline_risk', 0.0),
            project_data.get('team_stability', 0.5),
            project_data.get('technical_complexity', 0.5),
            project_data.get('stakeholder_risk', 0.0),
            project_data.get('regulatory_compliance', 0.5),
            project_data.get('resource_availability', 0.5),
            project_data.get('market_volatility', 0.0),
            project_data.get('political_risk', 0.0),
            project_data.get('reputation_risk', 0.0)
        ]

    def _get_grant_feature_names(self) -> List[str]:
        """Get feature names for grant prediction."""
        return [
            'normalized_budget', 'normalized_timeline', 'team_size',
            'partnership_count', 'experience_years', 'success_rate',
            'sdg_alignment_count', 'innovation_score', 'community_impact',
            'sustainability_score'
        ]

    def _get_impact_feature_names(self) -> List[str]:
        """Get feature names for impact prediction."""
        return [
            'normalized_funding', 'normalized_duration', 'participant_count',
            'geographic_reach', 'stakeholder_engagement', 'methodology_quality',
            'baseline_data_quality', 'evaluation_plan_quality', 'partnership_strength',
            'innovation_level'
        ]

    def _get_risk_feature_names(self) -> List[str]:
        """Get feature names for risk assessment."""
        return [
            'budget_volatility', 'timeline_risk', 'team_stability',
            'technical_complexity', 'stakeholder_risk', 'regulatory_compliance',
            'resource_availability', 'market_volatility', 'political_risk',
            'reputation_risk'
        ]

    async def _get_or_train_model(self, model_name: str, features: List[float]) -> Any:
        """Get trained model or train if not available."""
        model_path = os.path.join(self.models_dir, f"{model_name}.joblib")
        scaler_path = os.path.join(self.models_dir, f"{model_name}_scaler.joblib")

        if os.path.exists(model_path) and os.path.exists(scaler_path):
            # Load existing model
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)
            self.models[model_name] = model
            self.scalers[model_name] = scaler
        else:
            # Train new model with synthetic data
            await self._train_model_with_synthetic_data(model_name)

        return self.models[model_name]

    async def _train_model_with_synthetic_data(self, model_name: str):
        """Train model with synthetic data for demonstration."""
        # Generate synthetic training data
        n_samples = 1000
        n_features = 10

        # Generate features
        X = np.random.randn(n_samples, n_features)

        # Generate targets based on model type
        if model_name == 'grant_success':
            y = (X[:, 0] + X[:, 1] + X[:, 2] > 0).astype(int)  # Binary classification
        elif model_name == 'impact_outcome':
            y = np.clip(X[:, 0] * 2 + X[:, 1] * 1.5 + X[:, 2], 0, 10)  # Regression (0-10)
        elif model_name == 'rule_performance':
            y = np.clip(X[:, 0] * 0.8 + X[:, 1] * 0.6 + X[:, 2] * 0.4, 0, 1)  # Regression (0-1)
        elif model_name == 'risk_assessment':
            y = (X[:, 0] + X[:, 1] + X[:, 2] > 0.5).astype(int)  # Binary classification
        else:
            y = np.random.rand(n_samples)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Train model
        model = self.models[model_name]
        model.fit(X_train_scaled, y_train)

        # Evaluate model
        y_pred = model.predict(X_test_scaled)
        if hasattr(model, 'predict_proba'):
            accuracy = accuracy_score(y_test, y_pred)
            logger.info(f"{model_name} model accuracy: {accuracy:.3f}")
        else:
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            logger.info(f"{model_name} model MSE: {mse:.3f}, R²: {r2:.3f}")

        # Save model and scaler
        joblib.dump(model, os.path.join(self.models_dir, f"{model_name}.joblib"))
        joblib.dump(scaler, os.path.join(self.models_dir, f"{model_name}_scaler.joblib"))

        # Store feature importance if available
        if hasattr(model, 'feature_importances_'):
            self.feature_importance[model_name] = model.feature_importances_.tolist()

    def _calculate_confidence(self, model: Any, features: List[float]) -> float:
        """Calculate prediction confidence."""
        try:
            if hasattr(model, 'predict_proba'):
                # For classification models
                proba = model.predict_proba([features])[0]
                confidence = max(proba)
            else:
                # For regression models, use model's internal confidence if available
                confidence = 0.8  # Default confidence for regression
        except:
            confidence = 0.7  # Fallback confidence

        return min(confidence, 0.95)  # Cap at 95%

    def _determine_optimization_type(self, rule_data: Dict[str, Any]) -> str:
        """Determine the type of optimization needed."""
        if rule_data.get('error_rate', 0) > 0.1:
            return "error_reduction"
        elif rule_data.get('average_execution_time', 100) > 500:
            return "performance_optimization"
        elif rule_data.get('success_rate', 0.5) < 0.7:
            return "accuracy_improvement"
        else:
            return "general_optimization"

    def _generate_optimization_reasoning(self, rule_data: Dict[str, Any], improvement: float) -> str:
        """Generate reasoning for optimization recommendation."""
        rule_name = rule_data.get('rule_name', 'unknown')

        if improvement > 0.3:
            return f"High improvement potential ({improvement:.1%}) for {rule_name}. Consider rule restructuring."
        elif improvement > 0.2:
            return f"Moderate improvement potential ({improvement:.1%}) for {rule_name}. Consider parameter tuning."
        else:
            return f"Minor improvement potential ({improvement:.1%}) for {rule_name}. Consider monitoring."

    async def get_model_performance(self) -> Dict[str, Any]:
        """Get performance metrics for all models."""
        performance = {}

        for model_name in self.models.keys():
            model_path = os.path.join(self.models_dir, f"{model_name}.joblib")
            if os.path.exists(model_path):
                performance[model_name] = {
                    "status": "trained",
                    "last_updated": datetime.fromtimestamp(os.path.getmtime(model_path)).isoformat(),
                    "feature_importance": self.feature_importance.get(model_name, []),
                    "model_type": type(self.models[model_name]).__name__
                }
            else:
                performance[model_name] = {
                    "status": "not_trained",
                    "last_updated": None,
                    "feature_importance": [],
                    "model_type": type(self.models[model_name]).__name__
                }

        return performance

# Global ML engine instance
_ml_engine: Optional[AdvancedMLEngine] = None

def get_ml_engine() -> AdvancedMLEngine:
    """Get global ML engine instance."""
    global _ml_engine
    if _ml_engine is None:
        _ml_engine = AdvancedMLEngine()
    return _ml_engine
