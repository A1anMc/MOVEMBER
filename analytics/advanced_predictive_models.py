"""
Advanced Predictive Analytics for Movember
Sophisticated ML models for impact prediction, risk assessment, and optimization
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import json
import logging
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelType(Enum):
    """Types of predictive models"""
    IMPACT_PREDICTION = "impact_prediction"
    RISK_ASSESSMENT = "risk_assessment"
    ENGAGEMENT_FORECAST = "engagement_forecast"
    DONATION_PREDICTION = "donation_prediction"
    HEALTH_OUTCOME_PREDICTION = "health_outcome_prediction"
    CAMPAIGN_OPTIMIZATION = "campaign_optimization"
    AUDIENCE_SEGMENTATION = "audience_segmentation"
    CHURN_PREDICTION = "churn_prediction"

class PredictionHorizon(Enum):
    """Prediction time horizons"""
    SHORT_TERM = "short_term"  # 1-3 months
    MEDIUM_TERM = "medium_term"  # 3-12 months
    LONG_TERM = "long_term"  # 1-5 years

@dataclass
class ModelPerformance:
    """Model performance metrics"""
    model_type: ModelType
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    mse: float
    r2_score: float
    training_time: float
    prediction_time: float
    last_updated: datetime = field(default_factory=datetime.now)

@dataclass
class PredictionResult:
    """Prediction result with confidence intervals"""
    predicted_value: float
    confidence_interval_lower: float
    confidence_interval_upper: float
    confidence_level: float
    model_used: ModelType
    prediction_horizon: PredictionHorizon
    features_used: List[str]
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class FeatureImportance:
    """Feature importance for model interpretability"""
    feature_name: str
    importance_score: float
    rank: int
    category: str

@dataclass
class ModelInsight:
    """Insights derived from model analysis"""
    insight_type: str
    description: str
    confidence: float
    actionable: bool
    impact_score: float
    recommendations: List[str] = field(default_factory=list)

@dataclass
class AdvancedAnalyticsConfig:
    """Configuration for advanced analytics"""
    enable_real_time_predictions: bool = True
    enable_automated_retraining: bool = True
    retraining_frequency_days: int = 30
    confidence_threshold: float = 0.8
    max_features: int = 50
    cross_validation_folds: int = 5
    enable_feature_engineering: bool = True
    enable_ensemble_models: bool = True

class AdvancedPredictiveModels:
    """
    Advanced predictive analytics system for Movember
    Implements sophisticated ML models for various prediction tasks
    """
    
    def __init__(self, config: Optional[AdvancedAnalyticsConfig] = None):
        self.config = config or AdvancedAnalyticsConfig()
        self.models = {}
        self.scalers = {}
        self.feature_importance = {}
        self.performance_metrics = {}
        self.last_training = {}
        
        # Initialize models
        self._initialize_models()
        
    def _initialize_models(self):
        """Initialize all predictive models"""
        logger.info("Initializing advanced predictive models...")
        
        # Impact Prediction Models
        self.models[ModelType.IMPACT_PREDICTION] = {
            PredictionHorizon.SHORT_TERM: GradientBoostingRegressor(n_estimators=100, random_state=42),
            PredictionHorizon.MEDIUM_TERM: RandomForestRegressor(n_estimators=200, random_state=42),
            PredictionHorizon.LONG_TERM: GradientBoostingRegressor(n_estimators=300, random_state=42)
        }
        
        # Risk Assessment Models
        self.models[ModelType.RISK_ASSESSMENT] = {
            PredictionHorizon.SHORT_TERM: LogisticRegression(random_state=42),
            PredictionHorizon.MEDIUM_TERM: RandomForestRegressor(n_estimators=100, random_state=42),
            PredictionHorizon.LONG_TERM: GradientBoostingRegressor(n_estimators=200, random_state=42)
        }
        
        # Engagement Forecast Models
        self.models[ModelType.ENGAGEMENT_FORECAST] = {
            PredictionHorizon.SHORT_TERM: LinearRegression(),
            PredictionHorizon.MEDIUM_TERM: RandomForestRegressor(n_estimators=150, random_state=42),
            PredictionHorizon.LONG_TERM: GradientBoostingRegressor(n_estimators=250, random_state=42)
        }
        
        # Donation Prediction Models
        self.models[ModelType.DONATION_PREDICTION] = {
            PredictionHorizon.SHORT_TERM: RandomForestRegressor(n_estimators=100, random_state=42),
            PredictionHorizon.MEDIUM_TERM: GradientBoostingRegressor(n_estimators=200, random_state=42),
            PredictionHorizon.LONG_TERM: RandomForestRegressor(n_estimators=300, random_state=42)
        }
        
        # Health Outcome Prediction Models
        self.models[ModelType.HEALTH_OUTCOME_PREDICTION] = {
            PredictionHorizon.SHORT_TERM: LogisticRegression(random_state=42),
            PredictionHorizon.MEDIUM_TERM: RandomForestRegressor(n_estimators=100, random_state=42),
            PredictionHorizon.LONG_TERM: GradientBoostingRegressor(n_estimators=200, random_state=42)
        }
        
        # Campaign Optimization Models
        self.models[ModelType.CAMPAIGN_OPTIMIZATION] = {
            PredictionHorizon.SHORT_TERM: LinearRegression(),
            PredictionHorizon.MEDIUM_TERM: RandomForestRegressor(n_estimators=150, random_state=42),
            PredictionHorizon.LONG_TERM: GradientBoostingRegressor(n_estimators=250, random_state=42)
        }
        
        # Audience Segmentation Models
        self.models[ModelType.AUDIENCE_SEGMENTATION] = {
            PredictionHorizon.SHORT_TERM: KMeans(n_clusters=5, random_state=42),
            PredictionHorizon.MEDIUM_TERM: KMeans(n_clusters=7, random_state=42),
            PredictionHorizon.LONG_TERM: KMeans(n_clusters=10, random_state=42)
        }
        
        # Churn Prediction Models
        self.models[ModelType.CHURN_PREDICTION] = {
            PredictionHorizon.SHORT_TERM: LogisticRegression(random_state=42),
            PredictionHorizon.MEDIUM_TERM: RandomForestRegressor(n_estimators=100, random_state=42),
            PredictionHorizon.LONG_TERM: GradientBoostingRegressor(n_estimators=200, random_state=42)
        }
        
        # Initialize scalers for each model type
        for model_type in ModelType:
            self.scalers[model_type] = StandardScaler()
            
        logger.info(f"Initialized {len(self.models)} model types with {len(PredictionHorizon)} horizons each")
    
    def _generate_synthetic_data(self, model_type: ModelType, horizon: PredictionHorizon) -> Tuple[np.ndarray, np.ndarray]:
        """Generate synthetic training data for models"""
        np.random.seed(42)
        
        # Base features for all models
        n_samples = 1000 if horizon == PredictionHorizon.SHORT_TERM else 2000 if horizon == PredictionHorizon.MEDIUM_TERM else 3000
        
        # Common features
        features = {
            'campaign_budget': np.random.uniform(10000, 1000000, n_samples),
            'social_media_reach': np.random.uniform(1000, 1000000, n_samples),
            'email_subscribers': np.random.uniform(100, 100000, n_samples),
            'website_traffic': np.random.uniform(1000, 500000, n_samples),
            'donor_count': np.random.uniform(100, 50000, n_samples),
            'volunteer_count': np.random.uniform(10, 5000, n_samples),
            'event_count': np.random.uniform(1, 100, n_samples),
            'partnership_count': np.random.uniform(1, 50, n_samples),
            'media_coverage': np.random.uniform(0, 100, n_samples),
            'awareness_score': np.random.uniform(0, 100, n_samples)
        }
        
        # Model-specific features and targets
        if model_type == ModelType.IMPACT_PREDICTION:
            features.update({
                'lives_impacted': np.random.uniform(100, 100000, n_samples),
                'health_screenings': np.random.uniform(10, 10000, n_samples),
                'research_funding': np.random.uniform(10000, 1000000, n_samples)
            })
            target = features['lives_impacted'] * 0.3 + features['health_screenings'] * 0.2 + features['research_funding'] * 0.1 + np.random.normal(0, 1000, n_samples)
            
        elif model_type == ModelType.RISK_ASSESSMENT:
            features.update({
                'compliance_score': np.random.uniform(0, 100, n_samples),
                'financial_health': np.random.uniform(0, 100, n_samples),
                'reputation_score': np.random.uniform(0, 100, n_samples)
            })
            target = (features['compliance_score'] < 70) | (features['financial_health'] < 60) | (features['reputation_score'] < 80)
            
        elif model_type == ModelType.ENGAGEMENT_FORECAST:
            features.update({
                'social_engagement_rate': np.random.uniform(0, 10, n_samples),
                'email_open_rate': np.random.uniform(0, 50, n_samples),
                'event_attendance_rate': np.random.uniform(0, 100, n_samples)
            })
            target = features['social_engagement_rate'] * 0.4 + features['email_open_rate'] * 0.3 + features['event_attendance_rate'] * 0.3 + np.random.normal(0, 5, n_samples)
            
        elif model_type == ModelType.DONATION_PREDICTION:
            features.update({
                'avg_donation_amount': np.random.uniform(10, 500, n_samples),
                'donor_retention_rate': np.random.uniform(0, 100, n_samples),
                'major_donor_count': np.random.uniform(0, 100, n_samples)
            })
            target = features['avg_donation_amount'] * features['donor_count'] * (features['donor_retention_rate'] / 100) + np.random.normal(0, 10000, n_samples)
            
        elif model_type == ModelType.HEALTH_OUTCOME_PREDICTION:
            features.update({
                'screening_rate': np.random.uniform(0, 100, n_samples),
                'early_detection_rate': np.random.uniform(0, 100, n_samples),
                'survival_rate': np.random.uniform(0, 100, n_samples)
            })
            target = (features['screening_rate'] > 70) & (features['early_detection_rate'] > 60) & (features['survival_rate'] > 80)
            
        elif model_type == ModelType.CAMPAIGN_OPTIMIZATION:
            features.update({
                'roi': np.random.uniform(0, 10, n_samples),
                'conversion_rate': np.random.uniform(0, 20, n_samples),
                'cost_per_acquisition': np.random.uniform(10, 500, n_samples)
            })
            target = features['roi'] * 0.5 + features['conversion_rate'] * 0.3 + (1000 / features['cost_per_acquisition']) * 0.2 + np.random.normal(0, 1, n_samples)
            
        elif model_type == ModelType.AUDIENCE_SEGMENTATION:
            features.update({
                'age_group': np.random.randint(18, 80, n_samples),
                'income_level': np.random.randint(1, 10, n_samples),
                'engagement_frequency': np.random.uniform(0, 10, n_samples)
            })
            target = np.random.randint(0, 5, n_samples)  # 5 segments
            
        elif model_type == ModelType.CHURN_PREDICTION:
            features.update({
                'days_since_last_donation': np.random.uniform(0, 365, n_samples),
                'interaction_frequency': np.random.uniform(0, 10, n_samples),
                'satisfaction_score': np.random.uniform(0, 100, n_samples)
            })
            target = (features['days_since_last_donation'] > 180) | (features['satisfaction_score'] < 50)
        
        # Convert to numpy arrays
        X = np.column_stack([features[col] for col in sorted(features.keys())])
        y = target
        
        return X, y
    
    def train_model(self, model_type: ModelType, horizon: PredictionHorizon, force_retrain: bool = False) -> ModelPerformance:
        """Train a specific model"""
        model_key = f"{model_type.value}_{horizon.value}"
        
        # Check if retraining is needed
        if not force_retrain and model_key in self.last_training:
            days_since_training = (datetime.now() - self.last_training[model_key]).days
            if days_since_training < self.config.retraining_frequency_days:
                logger.info(f"Model {model_key} was trained {days_since_training} days ago, skipping retraining")
                return self.performance_metrics.get(model_key)
        
        logger.info(f"Training {model_key} model...")
        start_time = datetime.now()
        
        # Generate training data
        X, y = self._generate_synthetic_data(model_type, horizon)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        X_train_scaled = self.scalers[model_type].fit_transform(X_train)
        X_test_scaled = self.scalers[model_type].transform(X_test)
        
        # Get model
        model = self.models[model_type][horizon]
        
        # Train model
        model.fit(X_train_scaled, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test_scaled)
        
        # Calculate metrics
        training_time = (datetime.now() - start_time).total_seconds()
        
        if model_type in [ModelType.RISK_ASSESSMENT, ModelType.HEALTH_OUTCOME_PREDICTION, ModelType.CHURN_PREDICTION]:
            # Classification metrics
            accuracy = accuracy_score(y_test, y_pred)
            from sklearn.metrics import precision_recall_fscore_support
            precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='binary')
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
        else:
            # Regression metrics
            accuracy = r2_score(y_test, y_pred)
            precision = recall = f1 = 0.0  # Not applicable for regression
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
        
        # Store feature importance
        if hasattr(model, 'feature_importances_'):
            feature_names = [f"feature_{i}" for i in range(X.shape[1])]
            importances = model.feature_importances_
            self.feature_importance[model_key] = [
                FeatureImportance(
                    feature_name=name,
                    importance_score=score,
                    rank=i+1,
                    category="model_feature"
                )
                for i, (name, score) in enumerate(sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True))
            ]
        
        # Create performance metrics
        performance = ModelPerformance(
            model_type=model_type,
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1_score=f1,
            mse=mse,
            r2_score=r2,
            training_time=training_time,
            prediction_time=0.001  # Placeholder
        )
        
        self.performance_metrics[model_key] = performance
        self.last_training[model_key] = datetime.now()
        
        logger.info(f"Trained {model_key} model - R²: {r2:.3f}, MSE: {mse:.3f}")
        return performance
    
    def predict(self, model_type: ModelType, horizon: PredictionHorizon, features: Dict[str, float]) -> PredictionResult:
        """Make a prediction using the trained model"""
        model_key = f"{model_type.value}_{horizon.value}"
        
        # Ensure model is trained
        if model_key not in self.last_training:
            self.train_model(model_type, horizon)
        
        # Prepare features
        feature_names = sorted(features.keys())
        X = np.array([[features[name] for name in feature_names]]).reshape(1, -1)
        
        # Scale features
        X_scaled = self.scalers[model_type].transform(X)
        
        # Make prediction
        model = self.models[model_type][horizon]
        prediction = model.predict(X_scaled)[0]
        
        # Calculate confidence interval (simplified)
        confidence_level = 0.95
        confidence_range = 0.1 * abs(prediction)  # 10% of prediction value
        
        result = PredictionResult(
            predicted_value=float(prediction),
            confidence_interval_lower=float(prediction - confidence_range),
            confidence_interval_upper=float(prediction + confidence_range),
            confidence_level=confidence_level,
            model_used=model_type,
            prediction_horizon=horizon,
            features_used=feature_names
        )
        
        return result
    
    def generate_insights(self, model_type: ModelType, horizon: PredictionHorizon) -> List[ModelInsight]:
        """Generate insights from model analysis"""
        model_key = f"{model_type.value}_{horizon.value}"
        
        insights = []
        
        # Performance insights
        if model_key in self.performance_metrics:
            perf = self.performance_metrics[model_key]
            
            if perf.r2_score > 0.8:
                insights.append(ModelInsight(
                    insight_type="model_performance",
                    description=f"Excellent model performance with R² = {perf.r2_score:.3f}",
                    confidence=0.9,
                    actionable=True,
                    impact_score=0.8,
                    recommendations=["Model is ready for production use", "Consider using for critical decisions"]
                ))
            elif perf.r2_score > 0.6:
                insights.append(ModelInsight(
                    insight_type="model_performance",
                    description=f"Good model performance with R² = {perf.r2_score:.3f}",
                    confidence=0.7,
                    actionable=True,
                    impact_score=0.6,
                    recommendations=["Model can be used with caution", "Consider feature engineering to improve performance"]
                ))
            else:
                insights.append(ModelInsight(
                    insight_type="model_performance",
                    description=f"Poor model performance with R² = {perf.r2_score:.3f}",
                    confidence=0.8,
                    actionable=True,
                    impact_score=0.3,
                    recommendations=["Model needs improvement", "Consider collecting more data", "Review feature selection"]
                ))
        
        # Feature importance insights
        if model_key in self.feature_importance:
            top_features = self.feature_importance[model_key][:5]
            
            insights.append(ModelInsight(
                insight_type="feature_importance",
                description=f"Top features: {', '.join([f.feature_name for f in top_features])}",
                confidence=0.8,
                actionable=True,
                impact_score=0.7,
                recommendations=[
                    f"Focus on {top_features[0].feature_name} for maximum impact",
                    "Consider collecting more data on top features",
                    "Optimize campaigns based on feature importance"
                ]
            ))
        
        return insights
    
    def train_all_models(self) -> Dict[str, ModelPerformance]:
        """Train all models"""
        logger.info("Training all advanced predictive models...")
        
        performances = {}
        for model_type in ModelType:
            for horizon in PredictionHorizon:
                try:
                    perf = self.train_model(model_type, horizon)
                    model_key = f"{model_type.value}_{horizon.value}"
                    performances[model_key] = perf
                except Exception as e:
                    logger.error(f"Error training {model_type.value}_{horizon.value}: {e}")
        
        logger.info(f"Trained {len(performances)} models successfully")
        return performances
    
    def get_model_summary(self) -> Dict[str, Any]:
        """Get summary of all models"""
        summary = {
            "total_models": len(ModelType) * len(PredictionHorizon),
            "trained_models": len(self.last_training),
            "model_types": [mt.value for mt in ModelType],
            "prediction_horizons": [ph.value for ph in PredictionHorizon],
            "average_performance": {},
            "recent_training": {},
            "insights_count": 0
        }
        
        # Calculate average performance by model type
        for model_type in ModelType:
            type_performances = []
            for horizon in PredictionHorizon:
                model_key = f"{model_type.value}_{horizon.value}"
                if model_key in self.performance_metrics:
                    type_performances.append(self.performance_metrics[model_key].r2_score)
            
            if type_performances:
                summary["average_performance"][model_type.value] = {
                    "avg_r2": np.mean(type_performances),
                    "avg_mse": np.mean([self.performance_metrics[f"{model_type.value}_{ph.value}"].mse 
                                      for ph in PredictionHorizon 
                                      if f"{model_type.value}_{ph.value}" in self.performance_metrics])
                }
        
        # Recent training info
        for model_key, last_training in self.last_training.items():
            days_ago = (datetime.now() - last_training).days
            summary["recent_training"][model_key] = f"{days_ago} days ago"
        
        # Count insights
        for model_type in ModelType:
            for horizon in PredictionHorizon:
                insights = self.generate_insights(model_type, horizon)
                summary["insights_count"] += len(insights)
        
        return summary
    
    def export_model_data(self) -> Dict[str, Any]:
        """Export all model data for persistence"""
        return {
            "config": {
                "enable_real_time_predictions": self.config.enable_real_time_predictions,
                "enable_automated_retraining": self.config.enable_automated_retraining,
                "retraining_frequency_days": self.config.retraining_frequency_days,
                "confidence_threshold": self.config.confidence_threshold,
                "max_features": self.config.max_features,
                "cross_validation_folds": self.config.cross_validation_folds,
                "enable_feature_engineering": self.config.enable_feature_engineering,
                "enable_ensemble_models": self.config.enable_ensemble_models
            },
            "performance_metrics": {
                key: {
                    "model_type": perf.model_type.value,
                    "accuracy": perf.accuracy,
                    "precision": perf.precision,
                    "recall": perf.recall,
                    "f1_score": perf.f1_score,
                    "mse": perf.mse,
                    "r2_score": perf.r2_score,
                    "training_time": perf.training_time,
                    "prediction_time": perf.prediction_time,
                    "last_updated": perf.last_updated.isoformat()
                }
                for key, perf in self.performance_metrics.items()
            },
            "last_training": {
                key: value.isoformat() for key, value in self.last_training.items()
            },
            "feature_importance": {
                key: [
                    {
                        "feature_name": fi.feature_name,
                        "importance_score": fi.importance_score,
                        "rank": fi.rank,
                        "category": fi.category
                    }
                    for fi in importance_list
                ]
                for key, importance_list in self.feature_importance.items()
            }
        }

# Example usage and testing
if __name__ == "__main__":
    # Initialize advanced predictive models
    advanced_models = AdvancedPredictiveModels()
    
    # Train all models
    performances = advanced_models.train_all_models()
    
    # Get model summary
    summary = advanced_models.get_model_summary()
    print("Advanced Predictive Models Summary:")
    print(json.dumps(summary, indent=2))
    
    # Example prediction
    sample_features = {
        'campaign_budget': 500000,
        'social_media_reach': 100000,
        'email_subscribers': 50000,
        'website_traffic': 100000,
        'donor_count': 10000,
        'volunteer_count': 500,
        'event_count': 20,
        'partnership_count': 15,
        'media_coverage': 50,
        'awareness_score': 75
    }
    
    prediction = advanced_models.predict(
        ModelType.IMPACT_PREDICTION,
        PredictionHorizon.MEDIUM_TERM,
        sample_features
    )
    
    print(f"\nImpact Prediction (Medium Term):")
    print(f"Predicted Value: {prediction.predicted_value:,.0f}")
    print(f"Confidence Interval: {prediction.confidence_interval_lower:,.0f} - {prediction.confidence_interval_upper:,.0f}")
    print(f"Confidence Level: {prediction.confidence_level:.1%}")
    
    # Generate insights
    insights = advanced_models.generate_insights(ModelType.IMPACT_PREDICTION, PredictionHorizon.MEDIUM_TERM)
    print(f"\nGenerated {len(insights)} insights")
    for insight in insights:
        print(f"- {insight.description}")
