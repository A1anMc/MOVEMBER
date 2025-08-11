#!/usr/bin/env python3
"""
Predictive Analytics Engine
Advanced machine learning models for Movember impact prediction and optimization.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd

logger = logging.getLogger(__name__)

class PredictionType(Enum):
    GRANT_SUCCESS = "grant_success"
    IMPACT_GROWTH = "impact_growth"
    FUNDING_TREND = "funding_trend"
    PARTICIPATION_RATE = "participation_rate"
    RESEARCH_OUTCOME = "research_outcome"

class ModelType(Enum):
    RANDOM_FOREST = "random_forest"
    GRADIENT_BOOSTING = "gradient_boosting"
    LINEAR_REGRESSION = "linear_regression"
    ENSEMBLE = "ensemble"

@dataclass
class PredictionResult:
    """Result of a prediction model."""
    prediction_type: PredictionType
    model_type: ModelType
    predicted_value: float
    confidence: float
    features_used: List[str]
    timestamp: datetime
    metadata: Dict[str, Any]

@dataclass
class TrendAnalysis:
    """Analysis of historical trends."""
    metric_name: str
    current_value: float
    trend_direction: str  # "increasing", "decreasing", "stable"
    trend_strength: float  # 0-1
    seasonal_pattern: Optional[str]
    forecast_3_months: float
    forecast_6_months: float
    forecast_12_months: float
    confidence_intervals: Dict[str, Tuple[float, float]]

class PredictiveAnalyticsEngine:
    """Advanced predictive analytics for Movember impact optimization."""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.feature_importance = {}
        self.historical_data = {}
        self.model_performance = {}
        
    async def initialize_models(self):
        """Initialize all prediction models."""
        logger.info("Initializing predictive analytics models...")
        
        # Initialize models for each prediction type
        for pred_type in PredictionType:
            self.models[pred_type] = {
                ModelType.RANDOM_FOREST: RandomForestRegressor(n_estimators=100, random_state=42),
                ModelType.GRADIENT_BOOSTING: GradientBoostingRegressor(n_estimators=100, random_state=42),
                ModelType.LINEAR_REGRESSION: LinearRegression()
            }
            self.scalers[pred_type] = StandardScaler()
            
        logger.info("Predictive models initialized successfully")
    
    async def load_historical_data(self) -> Dict[str, pd.DataFrame]:
        """Load and prepare historical data for training."""
        logger.info("Loading historical data for model training...")
        
        # Simulate historical data (in production, this would come from databases)
        historical_data = {
            "grant_success": self._generate_grant_data(),
            "impact_metrics": self._generate_impact_data(),
            "funding_data": self._generate_funding_data(),
            "participation_data": self._generate_participation_data(),
            "research_data": self._generate_research_data()
        }
        
        self.historical_data = historical_data
        logger.info(f"Loaded {len(historical_data)} historical datasets")
        return historical_data
    
    def _generate_grant_data(self) -> pd.DataFrame:
        """Generate synthetic grant success data."""
        np.random.seed(42)
        n_samples = 1000
        
        data = {
            'budget_amount': np.random.uniform(50000, 500000, n_samples),
            'team_size': np.random.randint(1, 20, n_samples),
            'experience_years': np.random.uniform(1, 25, n_samples),
            'previous_grants': np.random.randint(0, 10, n_samples),
            'research_quality_score': np.random.uniform(5, 10, n_samples),
            'collaboration_score': np.random.uniform(3, 10, n_samples),
            'innovation_score': np.random.uniform(4, 10, n_samples),
            'impact_potential': np.random.uniform(6, 10, n_samples),
            'geographic_reach': np.random.randint(1, 50, n_samples),
            'timeline_months': np.random.randint(6, 36, n_samples)
        }
        
        # Calculate success probability based on features
        success_prob = (
            data['research_quality_score'] * 0.3 +
            data['impact_potential'] * 0.25 +
            data['experience_years'] * 0.02 +
            data['previous_grants'] * 0.05 +
            data['collaboration_score'] * 0.15 +
            data['innovation_score'] * 0.15 +
            np.random.normal(0, 0.1, n_samples)
        )
        
        data['success_probability'] = np.clip(success_prob, 0, 1)
        data['grant_approved'] = (data['success_probability'] > 0.6).astype(int)
        
        return pd.DataFrame(data)
    
    def _generate_impact_data(self) -> pd.DataFrame:
        """Generate synthetic impact metrics data."""
        np.random.seed(42)
        n_samples = 500
        
        # Generate time series data
        dates = pd.date_range(start='2020-01-01', periods=n_samples, freq='M')
        
        # Base trends with seasonal patterns
        base_trend = np.linspace(100, 200, n_samples)
        seasonal = 20 * np.sin(2 * np.pi * np.arange(n_samples) / 12)
        noise = np.random.normal(0, 5, n_samples)
        
        data = {
            'date': dates,
            'people_reached': base_trend + seasonal + noise,
            'funding_raised': base_trend * 1000 + seasonal * 500 + noise * 100,
            'research_projects': base_trend / 10 + seasonal / 20 + noise / 10,
            'volunteer_hours': base_trend * 50 + seasonal * 25 + noise * 10,
            'awareness_score': base_trend / 2 + seasonal / 4 + noise / 2
        }
        
        return pd.DataFrame(data)
    
    def _generate_funding_data(self) -> pd.DataFrame:
        """Generate synthetic funding trend data."""
        np.random.seed(42)
        n_samples = 300
        
        dates = pd.date_range(start='2020-01-01', periods=n_samples, freq='M')
        
        # Exponential growth with seasonal patterns
        base_growth = 1000000 * np.exp(0.02 * np.arange(n_samples))
        seasonal = 100000 * np.sin(2 * np.pi * np.arange(n_samples) / 12)
        noise = np.random.normal(0, 50000, n_samples)
        
        data = {
            'date': dates,
            'total_funding': base_growth + seasonal + noise,
            'individual_donations': base_growth * 0.6 + seasonal * 0.5 + noise * 0.6,
            'corporate_sponsorships': base_growth * 0.3 + seasonal * 0.3 + noise * 0.3,
            'grant_funding': base_growth * 0.1 + seasonal * 0.2 + noise * 0.1
        }
        
        return pd.DataFrame(data)
    
    def _generate_participation_data(self) -> pd.DataFrame:
        """Generate synthetic participation rate data."""
        np.random.seed(42)
        n_samples = 400
        
        dates = pd.date_range(start='2020-01-01', periods=n_samples, freq='M')
        
        # Logistic growth with seasonal peaks
        base_participation = 1000000 / (1 + np.exp(-0.1 * (np.arange(n_samples) - 200)))
        seasonal = 50000 * np.sin(2 * np.pi * np.arange(n_samples) / 12)
        noise = np.random.normal(0, 10000, n_samples)
        
        data = {
            'date': dates,
            'total_participants': base_participation + seasonal + noise,
            'new_registrations': np.diff(base_participation, prepend=base_participation[0]) + seasonal / 12 + noise / 10,
            'retention_rate': 0.7 + 0.1 * np.sin(2 * np.pi * np.arange(n_samples) / 12) + np.random.normal(0, 0.05, n_samples),
            'engagement_score': 0.6 + 0.2 * np.sin(2 * np.pi * np.arange(n_samples) / 12) + np.random.normal(0, 0.1, n_samples)
        }
        
        return pd.DataFrame(data)
    
    def _generate_research_data(self) -> pd.DataFrame:
        """Generate synthetic research outcome data."""
        np.random.seed(42)
        n_samples = 200
        
        data = {
            'research_budget': np.random.uniform(50000, 500000, n_samples),
            'team_expertise': np.random.uniform(5, 10, n_samples),
            'collaboration_level': np.random.uniform(3, 10, n_samples),
            'innovation_level': np.random.uniform(4, 10, n_samples),
            'timeline_months': np.random.randint(12, 60, n_samples),
            'publication_count': np.random.randint(0, 20, n_samples),
            'citation_count': np.random.randint(0, 100, n_samples),
            'clinical_trials': np.random.randint(0, 5, n_samples),
            'patents_filed': np.random.randint(0, 3, n_samples),
            'industry_partnerships': np.random.randint(0, 8, n_samples)
        }
        
        # Calculate research impact score
        impact_score = (
            data['publication_count'] * 0.2 +
            data['citation_count'] * 0.3 +
            data['clinical_trials'] * 0.25 +
            data['patents_filed'] * 0.15 +
            data['industry_partnerships'] * 0.1 +
            np.random.normal(0, 0.5, n_samples)
        )
        
        data['research_impact_score'] = np.clip(impact_score, 0, 10)
        
        return pd.DataFrame(data)
    
    async def train_models(self):
        """Train all prediction models."""
        logger.info("Training predictive models...")
        
        # Load historical data
        await self.load_historical_data()
        
        # Train grant success prediction model
        await self._train_grant_success_model()
        
        # Train impact growth prediction model
        await self._train_impact_growth_model()
        
        # Train funding trend prediction model
        await self._train_funding_trend_model()
        
        # Train participation rate prediction model
        await self._train_participation_model()
        
        # Train research outcome prediction model
        await self._train_research_outcome_model()
        
        logger.info("All models trained successfully")
    
    async def _train_grant_success_model(self):
        """Train grant success prediction model."""
        data = self.historical_data['grant_success']
        
        # Features for grant success prediction
        feature_columns = [
            'budget_amount', 'team_size', 'experience_years', 'previous_grants',
            'research_quality_score', 'collaboration_score', 'innovation_score',
            'impact_potential', 'geographic_reach', 'timeline_months'
        ]
        
        X = data[feature_columns]
        y = data['success_probability']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        X_train_scaled = self.scalers[PredictionType.GRANT_SUCCESS].fit_transform(X_train)
        X_test_scaled = self.scalers[PredictionType.GRANT_SUCCESS].transform(X_test)
        
        # Train models
        for model_type, model in self.models[PredictionType.GRANT_SUCCESS].items():
            model.fit(X_train_scaled, y_train)
            
            # Evaluate model
            y_pred = model.predict(X_test_scaled)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            self.model_performance[f"{PredictionType.GRANT_SUCCESS}_{model_type}"] = {
                'mse': mse,
                'r2': r2,
                'feature_importance': self._get_feature_importance(model, feature_columns)
            }
        
        self.feature_importance[PredictionType.GRANT_SUCCESS] = feature_columns
    
    async def _train_impact_growth_model(self):
        """Train impact growth prediction model."""
        data = self.historical_data['impact_metrics']
        
        # Create lagged features for time series prediction
        data['people_reached_lag1'] = data['people_reached'].shift(1)
        data['people_reached_lag2'] = data['people_reached'].shift(2)
        data['people_reached_lag3'] = data['people_reached'].shift(3)
        data['month'] = data['date'].dt.month
        data['quarter'] = data['date'].dt.quarter
        data['year'] = data['date'].dt.year
        
        # Remove NaN values
        data = data.dropna()
        
        feature_columns = [
            'people_reached_lag1', 'people_reached_lag2', 'people_reached_lag3',
            'funding_raised', 'research_projects', 'volunteer_hours',
            'awareness_score', 'month', 'quarter', 'year'
        ]
        
        X = data[feature_columns]
        y = data['people_reached']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        X_train_scaled = self.scalers[PredictionType.IMPACT_GROWTH].fit_transform(X_train)
        X_test_scaled = self.scalers[PredictionType.IMPACT_GROWTH].transform(X_test)
        
        # Train models
        for model_type, model in self.models[PredictionType.IMPACT_GROWTH].items():
            model.fit(X_train_scaled, y_train)
            
            # Evaluate model
            y_pred = model.predict(X_test_scaled)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            self.model_performance[f"{PredictionType.IMPACT_GROWTH}_{model_type}"] = {
                'mse': mse,
                'r2': r2,
                'feature_importance': self._get_feature_importance(model, feature_columns)
            }
        
        self.feature_importance[PredictionType.IMPACT_GROWTH] = feature_columns
    
    async def _train_funding_trend_model(self):
        """Train funding trend prediction model."""
        data = self.historical_data['funding_data']
        
        # Create lagged features
        data['total_funding_lag1'] = data['total_funding'].shift(1)
        data['total_funding_lag2'] = data['total_funding'].shift(2)
        data['month'] = data['date'].dt.month
        data['quarter'] = data['date'].dt.quarter
        data['year'] = data['date'].dt.year
        
        data = data.dropna()
        
        feature_columns = [
            'total_funding_lag1', 'total_funding_lag2',
            'individual_donations', 'corporate_sponsorships', 'grant_funding',
            'month', 'quarter', 'year'
        ]
        
        X = data[feature_columns]
        y = data['total_funding']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        X_train_scaled = self.scalers[PredictionType.FUNDING_TREND].fit_transform(X_train)
        X_test_scaled = self.scalers[PredictionType.FUNDING_TREND].transform(X_test)
        
        for model_type, model in self.models[PredictionType.FUNDING_TREND].items():
            model.fit(X_train_scaled, y_train)
            
            y_pred = model.predict(X_test_scaled)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            self.model_performance[f"{PredictionType.FUNDING_TREND}_{model_type}"] = {
                'mse': mse,
                'r2': r2,
                'feature_importance': self._get_feature_importance(model, feature_columns)
            }
        
        self.feature_importance[PredictionType.FUNDING_TREND] = feature_columns
    
    async def _train_participation_model(self):
        """Train participation rate prediction model."""
        data = self.historical_data['participation_data']
        
        data['total_participants_lag1'] = data['total_participants'].shift(1)
        data['total_participants_lag2'] = data['total_participants'].shift(2)
        data['month'] = data['date'].dt.month
        data['quarter'] = data['date'].dt.quarter
        data['year'] = data['date'].dt.year
        
        data = data.dropna()
        
        feature_columns = [
            'total_participants_lag1', 'total_participants_lag2',
            'new_registrations', 'retention_rate', 'engagement_score',
            'month', 'quarter', 'year'
        ]
        
        X = data[feature_columns]
        y = data['total_participants']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        X_train_scaled = self.scalers[PredictionType.PARTICIPATION_RATE].fit_transform(X_train)
        X_test_scaled = self.scalers[PredictionType.PARTICIPATION_RATE].transform(X_test)
        
        for model_type, model in self.models[PredictionType.PARTICIPATION_RATE].items():
            model.fit(X_train_scaled, y_train)
            
            y_pred = model.predict(X_test_scaled)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            self.model_performance[f"{PredictionType.PARTICIPATION_RATE}_{model_type}"] = {
                'mse': mse,
                'r2': r2,
                'feature_importance': self._get_feature_importance(model, feature_columns)
            }
        
        self.feature_importance[PredictionType.PARTICIPATION_RATE] = feature_columns
    
    async def _train_research_outcome_model(self):
        """Train research outcome prediction model."""
        data = self.historical_data['research_data']
        
        feature_columns = [
            'research_budget', 'team_expertise', 'collaboration_level',
            'innovation_level', 'timeline_months'
        ]
        
        X = data[feature_columns]
        y = data['research_impact_score']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        X_train_scaled = self.scalers[PredictionType.RESEARCH_OUTCOME].fit_transform(X_train)
        X_test_scaled = self.scalers[PredictionType.RESEARCH_OUTCOME].transform(X_test)
        
        for model_type, model in self.models[PredictionType.RESEARCH_OUTCOME].items():
            model.fit(X_train_scaled, y_train)
            
            y_pred = model.predict(X_test_scaled)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            self.model_performance[f"{PredictionType.RESEARCH_OUTCOME}_{model_type}"] = {
                'mse': mse,
                'r2': r2,
                'feature_importance': self._get_feature_importance(model, feature_columns)
            }
        
        self.feature_importance[PredictionType.RESEARCH_OUTCOME] = feature_columns
    
    def _get_feature_importance(self, model, feature_names: List[str]) -> Dict[str, float]:
        """Extract feature importance from trained model."""
        if hasattr(model, 'feature_importances_'):
            importance = model.feature_importances_
        elif hasattr(model, 'coef_'):
            importance = np.abs(model.coef_)
        else:
            importance = np.ones(len(feature_names)) / len(feature_names)
        
        return dict(zip(feature_names, importance))
    
    async def predict_grant_success(self, grant_data: Dict[str, Any]) -> PredictionResult:
        """Predict grant success probability."""
        # Prepare features
        features = [
            grant_data.get('budget_amount', 0),
            grant_data.get('team_size', 1),
            grant_data.get('experience_years', 5),
            grant_data.get('previous_grants', 0),
            grant_data.get('research_quality_score', 7),
            grant_data.get('collaboration_score', 7),
            grant_data.get('innovation_score', 7),
            grant_data.get('impact_potential', 7),
            grant_data.get('geographic_reach', 10),
            grant_data.get('timeline_months', 24)
        ]
        
        # Use best performing model
        best_model = self._get_best_model(PredictionType.GRANT_SUCCESS)
        features_scaled = self.scalers[PredictionType.GRANT_SUCCESS].transform([features])
        
        prediction = best_model.predict(features_scaled)[0]
        confidence = self._calculate_confidence(PredictionType.GRANT_SUCCESS, best_model)
        
        return PredictionResult(
            prediction_type=PredictionType.GRANT_SUCCESS,
            model_type=ModelType.RANDOM_FOREST,  # Assuming this is best
            predicted_value=prediction,
            confidence=confidence,
            features_used=self.feature_importance[PredictionType.GRANT_SUCCESS],
            timestamp=datetime.now(),
            metadata={'grant_data': grant_data}
        )
    
    async def predict_impact_growth(self, current_metrics: Dict[str, Any]) -> PredictionResult:
        """Predict impact growth over next 12 months."""
        # Prepare features based on current metrics
        features = [
            current_metrics.get('people_reached_lag1', 1000000),
            current_metrics.get('people_reached_lag2', 950000),
            current_metrics.get('people_reached_lag3', 900000),
            current_metrics.get('funding_raised', 150000000),
            current_metrics.get('research_projects', 450),
            current_metrics.get('volunteer_hours', 50000),
            current_metrics.get('awareness_score', 7.5),
            datetime.now().month,
            datetime.now().quarter,
            datetime.now().year
        ]
        
        best_model = self._get_best_model(PredictionType.IMPACT_GROWTH)
        features_scaled = self.scalers[PredictionType.IMPACT_GROWTH].transform([features])
        
        prediction = best_model.predict(features_scaled)[0]
        confidence = self._calculate_confidence(PredictionType.IMPACT_GROWTH, best_model)
        
        return PredictionResult(
            prediction_type=PredictionType.IMPACT_GROWTH,
            model_type=ModelType.GRADIENT_BOOSTING,
            predicted_value=prediction,
            confidence=confidence,
            features_used=self.feature_importance[PredictionType.IMPACT_GROWTH],
            timestamp=datetime.now(),
            metadata={'current_metrics': current_metrics}
        )
    
    def _get_best_model(self, prediction_type: PredictionType):
        """Get the best performing model for a prediction type."""
        best_r2 = -1
        best_model = None
        
        for model_type in ModelType:
            if model_type == ModelType.ENSEMBLE:
                continue
                
            performance_key = f"{prediction_type}_{model_type}"
            if performance_key in self.model_performance:
                r2 = self.model_performance[performance_key]['r2']
                if r2 > best_r2:
                    best_r2 = r2
                    best_model = self.models[prediction_type][model_type]
        
        return best_model or self.models[prediction_type][ModelType.RANDOM_FOREST]
    
    def _calculate_confidence(self, prediction_type: PredictionType, model) -> float:
        """Calculate confidence score for prediction."""
        # Simple confidence calculation based on model performance
        best_r2 = 0
        for model_type in ModelType:
            if model_type == ModelType.ENSEMBLE:
                continue
                
            performance_key = f"{prediction_type}_{model_type}"
            if performance_key in self.model_performance:
                r2 = self.model_performance[performance_key]['r2']
                best_r2 = max(best_r2, r2)
        
        return min(best_r2, 0.95)  # Cap at 95% confidence
    
    async def analyze_trends(self, metric_name: str, historical_values: List[float]) -> TrendAnalysis:
        """Analyze trends in historical data."""
        if len(historical_values) < 6:
            return TrendAnalysis(
                metric_name=metric_name,
                current_value=historical_values[-1] if historical_values else 0,
                trend_direction="stable",
                trend_strength=0.0,
                seasonal_pattern=None,
                forecast_3_months=historical_values[-1] if historical_values else 0,
                forecast_6_months=historical_values[-1] if historical_values else 0,
                forecast_12_months=historical_values[-1] if historical_values else 0,
                confidence_intervals={}
            )
        
        # Calculate trend
        x = np.arange(len(historical_values))
        slope, intercept = np.polyfit(x, historical_values, 1)
        
        # Determine trend direction and strength
        if slope > 0.01:
            trend_direction = "increasing"
        elif slope < -0.01:
            trend_direction = "decreasing"
        else:
            trend_direction = "stable"
        
        trend_strength = min(abs(slope) / np.std(historical_values), 1.0)
        
        # Simple forecasting
        current_value = historical_values[-1]
        forecast_3_months = current_value + slope * 3
        forecast_6_months = current_value + slope * 6
        forecast_12_months = current_value + slope * 12
        
        # Confidence intervals (simplified)
        std_error = np.std(historical_values) * 0.1
        confidence_intervals = {
            "3_months": (forecast_3_months - std_error, forecast_3_months + std_error),
            "6_months": (forecast_6_months - std_error, forecast_6_months + std_error),
            "12_months": (forecast_12_months - std_error, forecast_12_months + std_error)
        }
        
        return TrendAnalysis(
            metric_name=metric_name,
            current_value=current_value,
            trend_direction=trend_direction,
            trend_strength=trend_strength,
            seasonal_pattern="quarterly" if len(historical_values) >= 12 else None,
            forecast_3_months=forecast_3_months,
            forecast_6_months=forecast_6_months,
            forecast_12_months=forecast_12_months,
            confidence_intervals=confidence_intervals
        )
    
    async def get_model_performance_summary(self) -> Dict[str, Any]:
        """Get summary of all model performances."""
        summary = {
            'total_models': len(self.model_performance),
            'average_r2': np.mean([perf['r2'] for perf in self.model_performance.values()]),
            'best_performing_model': None,
            'model_details': {}
        }
        
        best_r2 = -1
        for model_name, performance in self.model_performance.items():
            summary['model_details'][model_name] = performance
            
            if performance['r2'] > best_r2:
                best_r2 = performance['r2']
                summary['best_performing_model'] = model_name
        
        return summary

# Convenience function for easy integration
async def get_predictive_analytics_engine() -> PredictiveAnalyticsEngine:
    """Get initialized predictive analytics engine."""
    engine = PredictiveAnalyticsEngine()
    await engine.initialize_models()
    await engine.train_models()
    return engine

if __name__ == "__main__":
    # Test the predictive analytics engine
    async def test():
        engine = await get_predictive_analytics_engine()
        
        # Test grant success prediction
        grant_data = {
            'budget_amount': 250000,
            'team_size': 8,
            'experience_years': 12,
            'previous_grants': 3,
            'research_quality_score': 8.5,
            'collaboration_score': 8.0,
            'innovation_score': 7.5,
            'impact_potential': 8.0,
            'geographic_reach': 15,
            'timeline_months': 24
        }
        
        prediction = await engine.predict_grant_success(grant_data)
        print(f"Grant Success Prediction: {prediction.predicted_value:.3f} (confidence: {prediction.confidence:.3f})")
        
        # Test impact growth prediction
        current_metrics = {
            'people_reached_lag1': 1200000,
            'people_reached_lag2': 1150000,
            'people_reached_lag3': 1100000,
            'funding_raised': 160000000,
            'research_projects': 480,
            'volunteer_hours': 55000,
            'awareness_score': 7.8
        }
        
        impact_prediction = await engine.predict_impact_growth(current_metrics)
        print(f"Impact Growth Prediction: {impact_prediction.predicted_value:.0f} people (confidence: {impact_prediction.confidence:.3f})")
        
        # Get performance summary
        performance = await engine.get_model_performance_summary()
        print(f"Model Performance Summary: {performance['average_r2']:.3f} average R²")
    
    asyncio.run(test())
